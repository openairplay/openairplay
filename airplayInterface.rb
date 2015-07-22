#!/usr/bin/env ruby

require "clap"
require_relative "airplay/lib/airplay/cli"
require_relative "airplay/lib/airplay/cli/version"

def listAirDevices
  Airplay::CLI.method(:list)
end

while cmd = STDIN.gets
  # remove whitespaces:
  cmd.chop!
  # if command is "exit", terminate:
  if cmd == "exit"
    break
  else
    # else evaluate command, send result to standard output:
    print eval(cmd),"\n"
    # and append [end] so that master knows it's the last line:
    print "[end]\n"
    # flush stdout to avoid buffering issues:
    STDOUT.flush
  end
end
