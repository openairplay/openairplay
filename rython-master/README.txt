Overview
========

If you've ever needed to use Ruby for a particular task, but wanted
to use Python as your primary language, *Rython* lets you easily
mix the two languages together.

*Why would I want to mix Ruby and Python?*  There are many reasons:

* you need a Ruby Gem that provides unique functionality which no Python module provides
* you need a simpler syntax for manipulating regular expressions
* you want to quickly bridge to code you've already written in Ruby

Quickstart
==========

In this example, we will use Watir (http://wtr.rubyforge.org), a high level web application
testing Gem that has no equivalent in Python. First, you need to declare a Ruby context that will run the Ruby code.::

    import rython
    
    ctx = rython.RubyContext(requires=["rubygems", "watir"])

Next, instantiate a Watir::Browser object and assign it to a Python variable.
The object will be an instance of rython.RubyProxy::

    my_browser = ctx("Watir::Browser.new")
    
    assert isinstance(my_browser, rython.RubyProxy)

And now we can call any method on the object instance as well.  This example grabs
a DIV element from the page by CSS ID 'foobar'.  We can then execute more Ruby
methods on the div_element if we want::

    div_element = my_browser("div(:id, 'foobar')")
    
    assert isinstance(div_element, rython.RubyProxy)
    
    exists_in_browser = div_element("exists?")

Advanced
========

There are deeper features you can take advantage of in Rython.

Calling methods with RubyProxy arguments
----------------------------------------

Let's say you have a Ruby method that takes a complex Ruby object.  This
object will be proxied in the Python context as a RubyProxy.  To pass
this object to a method, simply use the *repr* string substitution.  The
following example passes a RubyProxied Browser object to a method::

    my_browser = ctx("Watir::Browser.new")
    my_foobar = ctx("Foobar.new")
    
    my_foobar("method_that_takes_browser(%(browser)r)", browser=my_browser)

Rython will automatically convert a RubyProxy argument to the appropriate
Ruby expression that refers to the object in the Ruby context.

Apply monkeypatches to the context
----------------------------------

When instantiating a RubyContext, you can specify a 'setup' parameter that
contains raw Ruby code to execute after doing the require statements.  This
is perfect for adding monkeypatches to Ruby objects, or just performing additional
setup.

This example monkeypatches the String object with a 'to_safe_string' method.
This makes it easy to convert all strings into printable characters::

    import rython
    
    monkeypatches = '''
        class String
            GOOD_NONUNICODE_CHARS = (("A".."Z").to_a + ("a".."z").to_a + ("0".."9").to_a).to_a
            def to_safe_string
                final = ""
                each_char do |ch|
                    final += "#{ch}" if GOOD_NONUNICODE_CHARS.include? ch
                end
                final
            end
        end
        '''
        
    ctx = rython.RubyContext(setup=monkeypatches)

Running the context in debug mode
---------------------------------

This is helpful when Rython appears to be failing due to problems in the Ruby context.
By default, all logging messages are suppressed from the Ruby context.  You can reenable them by
setting the debug flag::

    import rython
    
    ctx = rython.RubyContext(debug=True)
    