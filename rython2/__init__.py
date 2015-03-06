# http://www.onlamp.com/pub/a/python/2001/01/17/xmlrpcserver.html

import os
import re
import sys
import time
import socket
import signal
import random
import tempfile
import xmlrpclib
import threading
import subprocess

def _is_valid_ruby_class_identifer(ruby_class):
    return bool(re.compile("([A-Za-z_]+(::)?)+").match(ruby_class))

def _random_ruby_context_address_indicator():
    return "".join([random.choice("ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789") for x in range(50)])


class RubyContext(object):
    
    def __init__(self, port=None, host="127.0.0.1", requires=None, setup=None, debug=False):
        
        # set up internal state
        self.__debug = debug
        self.__xmlrpc_server_proc = None
        self.__xmlrpc_client = None
        self.__max_tries = 50
        self.__allow_none = True
        self.__ruby_context_address_indicator = _random_ruby_context_address_indicator()
        self.__proxy_lookup = {}
        
        # set up Python XMLRPC arguments
        self.__python_verbose = False
        
        # set up Ruby XMLRPC arguments
        self.__ruby_port = port
        self.__ruby_host = host
        self.__ruby_max_connections = 4
        self.__ruby_audit = True
        if self.__debug:
            self.__ruby_stdlog = "$stdout"
            self.__ruby_audit = True
            self.__ruby_debug = True
        else:
            self.__ruby_stdlog = "StringIO.new"
            self.__ruby_debug = False
        
        # set up additional Ruby arguments
        self.__ruby_allow_nils = self.__allow_none
        self.__ruby_requires = requires or []
        self.__ruby_setup = setup or ""
        
        # install signal handling
        this = self
        for unload_signal in [signal.SIGINT]:
            original_sig_cb = signal.getsignal(unload_signal)
            def new_sig_cb(*args, **kwargs):
                this.unload()
                original_sig_cb(*args, **kwargs)
            signal.signal(unload_signal, new_sig_cb)
    
    def load(self):
        self.__ensure_started()
    
    def unload(self):
        if self.__xmlrpc_server_proc:
            self.__xmlrpc_client.registry.shutdown()
            os.waitpid(self.__xmlrpc_server_proc.pid, 0)
            self.__xmlrpc_server_proc = None
            self.__ruby_port = None
    
    def reload(self):
        unload()
        load()
    
    def get(self, ruby_class):
        self.__ensure_started()
        if not _is_valid_ruby_class_identifer(ruby_class=ruby_class):
            raise ValueError("invalid Ruby class name: %r" % ruby_class)
        ruby_context_address = self.__xmlrpc_client.registry.get_object(ruby_class)
        return RubyProxy(context=self, ruby_context_address=ruby_context_address)
    
    def module(self, ruby_module):
        self.__ensure_started()
        if not _is_valid_ruby_class_identifer(ruby_class=ruby_class):
            raise ValueError("invalid Ruby module name: %r" % ruby_class)
        ruby_context_address = self.__xmlrpc_client.registry.get_object(ruby_module)
        return RubyProxy(context=self, ruby_context_address=ruby_context_address)
        
    def evaluate_on_instance(self, ruby_context_address, code):
        self.__ensure_started()
        value = self.__xmlrpc_client.registry.evaluate_on_instance(ruby_context_address, code)
        return self.__transform_value(value)
    
    def __call__(self, code):
        self.__ensure_started()
        value = self.__xmlrpc_client.registry.evaluate(code)
        return self.__transform_value(value)
    
    def __transform_value(self, value):
        
        # check for special values, they come across the wire as lists
        if isinstance(value, [].__class__) and len(value) == 3:
            # this might be a Ruby context address
            if value[0] == self.__ruby_context_address_indicator:
                # it is a Ruby context address value
                ruby_class = value[1]
                ruby_context_address = value[2]
                proxy = self.__lookup_proxy(ruby_context_address=ruby_context_address)
                if proxy:
                    # we already had this proxy mapped
                    return proxy
                else:
                    # this proxy was auto-generated in Ruby, wrap it in a RubyProxy
                    # TODO: choose the right Python class? this will require metaclasses
                    proxy = RubyProxy(
                        context=self,
                        ruby_context_address=ruby_context_address,
                        )
                    self.__track_proxy(proxy=proxy, ruby_context_address=ruby_context_address)
                    return proxy
        
        # we never transformed it, just return the original value
        return value
    
    def __lookup_proxy(self, ruby_context_address):
        return self.__proxy_lookup.get(ruby_context_address, None)
        
    def __track_proxy(self, proxy, ruby_context_address):
        self.__proxy_lookup[ruby_context_address] = proxy
    
    def __choose_unused_port(self):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.bind((self.__ruby_host, 0))
        addr, port = s.getsockname()
        s.close()
        return port
            
    def __ensure_started(self):
        if not self.__xmlrpc_server_proc:
            
            # choose a port
            self.__ruby_port = self.__choose_unused_port()

            # create a temporary file to store the script in
            script = self.__create_script()
            dontcare, filename = tempfile.mkstemp()
            fd = open(filename, "w")
            try:
                fd.write(script)
            finally:
                fd.close()
            
            # build the subprocess arguments
            args = ["ruby", "-W0", filename]
            if self.__debug:
                # debug mode, allow all server output to be displayed
                print >> sys.stderr, "starting Ruby context on http://%s:%s/" % (self.__ruby_host, self.__ruby_port)
                self.__xmlrpc_server_proc = subprocess.Popen(args=args)
            else:
                # not debug mode, hide all server output
                if os.path.exists("nul:"):
                    stdout = open("nul:", "w")
                    stderr = open("nul:", "w")
                elif os.path.exists("/dev/null"):
                    stdout = open("/dev/null", "w")
                    stderr = open("/dev/null", "w")
                else:
                    stdout = None
                    stderr = subprocess.PIPE
                self.__xmlrpc_server_proc= subprocess.Popen(
                    args=args,
                    stdout=stdout,
                    stderr=stderr,
                    close_fds=True,
                    bufsize=2,
                    )
            
            # wait for the ruby server to start
            socket_available = False
            tries_remaining = self.__max_tries
            while not socket_available and tries_remaining > 0:
                try:
                    s = socket.socket()
                    s.connect((self.__ruby_host, self.__ruby_port))
                    s.close()
                    socket_available = True
                except socket.error, e:
                    socket_available = False
                time.sleep(0.1)
                tries_remaining -= 1
            
            # ruby server started, connect to it
            # TODO: basic HTTP AUTH?
            self.__xmlrpc_client = xmlrpclib.Server(
                uri="http://%s:%s/" % (self.__ruby_host, self.__ruby_port),
                verbose=self.__python_verbose,
                allow_none=self.__allow_none,
                )
    
    def __create_script(self):
        require_statements = "\n".join(["require %r" % rlib for rlib in self.__ruby_requires])
        script = '''
            require "xmlrpc/server"
            require "xmlrpc/create"
            
            %(require_statements)s
            
            %(setup)s
            
            module XMLRPC

                class Create
                    
                    def will_throw_serialization_exception(obj)
                        begin
                            conv2value(obj)
                            return false
                        rescue StandardError => e
                            return true
                        end
                    end
                    
                end

            end
                
            if %(allow_nils)s
                XMLRPC::Config.const_set(:ENABLE_NIL_CREATE, true)
            end
            
            module Rython
            
                class Registry
                
                    def initialize(server)
                        @server = server
                        @proxies = {}
                    end
                    
                    def get_object(name)
                        obj = eval(name)
                        ruby_context_address = generate_ruby_context_address(obj)
                        add_proxy(ruby_context_address, obj)
                        ruby_context_address
                    end
                
                    def evaluate_on_instance(ruby_context_address, code)
                        obj = @proxies[ruby_context_address]
                        if obj
                            obj.instance_eval(code)
                        else
                            raise StandardError, "no object exists at '#{ruby_context_address}'"
                        end
                    end
                    
                    def evaluate(code)
                        eval(code)
                    end
                    
                    def generate_ruby_context_address(obj)
                        "ruby\##{obj.class.to_s}[#{obj.object_id}]"
                    end
                    
                    def add_proxy(ruby_context_address, proxy)
                        @proxies[ruby_context_address] = proxy
                    end
                
                    def get_proxy(ruby_context_address)
                        @proxies[ruby_context_address]
                    end
                    
                    def get_ruby_context_address(proxy)
                        @proxies.index(proxy)
                    end
                
                    def shutdown
                        @server.shutdown
                    end
                
                end
                
                def self.registry=(val)
                    @registry = val
                end
                
                def self.registry
                    @registry
                end
            
                server = XMLRPC::Server.new(%(port)s, '%(host)s', %(max_connections)s, %(stdlog)s, %(audit)s, %(debug)s)
                server.add_introspection
                
                self.registry = Registry.new(server)
                server.add_handler("registry", self.registry)
            
                # check for serialization errors
                checker = XMLRPC::Create.new
                server.set_service_hook do |obj, *args|
                    
                    # call the method
                    retval = obj.call(*args)
                    
                    # try to get the Ruby context address for this object
                    ruby_context_address = Rython::registry.get_ruby_context_address(retval)
                    
                    if !ruby_context_address and checker.will_throw_serialization_exception(retval)
                        # automatically make it a RubyProxy in Python land
                        # TODO: if this is an Array, iterate through and add contexts for EACH
                        ruby_context_address = Rython::registry.generate_ruby_context_address(retval)
                        Rython::registry.add_proxy(ruby_context_address, retval)
                    end
                    
                    if ruby_context_address
                        # this is a RubyProxy in Python land, refer to it
                        [%(ruby_context_address_indicator)r, "#{retval.class.to_s}", "#{ruby_context_address}"]
                    
                    else
                        # this return value is fine, no need to wrap it up
                        retval
                    end
                end
                
                server.serve
            
            end
            ''' % dict(
                require_statements=require_statements,
                setup=self.__ruby_setup,
                port=self.__ruby_port,
                host=self.__ruby_host,
                max_connections=self.__ruby_max_connections,
                stdlog=self.__ruby_stdlog,
                audit=str(self.__ruby_audit).lower(), # True/False ==> true/false
                debug=str(self.__ruby_debug).lower(), # True/False ==> true/false
                allow_nils=str(self.__ruby_allow_nils).lower(), # True/False ==> true/false
                ruby_context_address_indicator=self.__ruby_context_address_indicator,
                )
        return script

    
class RubyProxy(object):
    
    ruby_context_address = property(lambda self: self.__ruby_context_address)
    
    def __init__(self, context, ruby_context_address):
        self.__context = context
        self.__ruby_context_address = ruby_context_address
    
    def __call__(self, code, *args, **kwargs):
        if args and kwargs:
            raise ValueError("cannot mix sequenced arguments with keyword arguments when calling to the Ruby context")
        if kwargs:
            transformed_kwargs = {}
            for k,v in kwargs.iteritems():
                transformed_kwargs[k] = self.__transform_argument(v)
            substituted_code = code % transformed_kwargs
        else:
            substituted_code = code % tuple([self.__transform_argument(a) for a in args])
        return self.__context.evaluate_on_instance(ruby_context_address=self.__ruby_context_address, code=substituted_code)
    
    def __getattr__(self, name):
        
        method_name = name
        context = self.__context
        transform_argument = self.__transform_argument
        
        # create a method proxy
        def method_proxy(*args):
            
            # transform all the arguments to things that xmlrpc
            # with the Rython module will understand
            transformed_args = [transform_argument(a) for a in args]
            
            # generate the code that executes this method
            code = "%(method_name)s(%(arguments)s)" % dict(
                method_name=method_name,
                arguments=", ".join([repr(a) for a in transformed_args]),
                )
            
            # evaluate this method in the context
            return context.evaluate_on_instance(ruby_context_address=self.__ruby_context_address, code=code)
        
        # return our method proxy
        return method_proxy
    
    def __transform_argument(self, arg):
        """outputs a representation of the object that can be
        interpreted in the Ruby context"""
        
        if hasattr(arg, "ruby_context_address"):
            class RubyExpression(object):
                def __repr__(self):
                    return "Rython::registry.get_proxy(%r)" % arg.ruby_context_address
            return RubyExpression()
        elif isinstance(arg, bool):
            class RubyBool(object):
                def __repr__(self):
                    return "true" if arg else "false"
            return RubyBool()
        elif arg is None:
            class RubyNil(object):
                def __repr__(self):
                    return "nil"
            return RubyNil()
        else:
            # http://www.tldp.org/HOWTO/XML-RPC-HOWTO/xmlrpc-howto-intro.html#xmlrpc-howto-types
            # TODO: complex array types (use xmlrpc.dumps)
            # TODO: struct types (use xmlrpc.dumps)
            # TODO: datetime types (DateTime.from_timestamp(<timestamp in unix time>))
            # TODO: error out on non-basic Python objects that don't have a ruby_context_address
            return arg

