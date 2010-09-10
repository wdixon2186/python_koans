#!/usr/bin/env python
# -*- coding: utf-8 -*-

import unittest
import re

import helper
from mockable_test_result import MockableTestResult

from libs.colorama import init, Fore
init()


class Sensei(MockableTestResult):
    def __init__(self, stream):
        unittest.TestResult.__init__(self)
        self.stream = stream
        self.prevTestClassName = None
        self.pass_count = 0

    def startTest(self, test):
        MockableTestResult.startTest(self, test)

        if helper.cls_name(test) != self.prevTestClassName:
            self.prevTestClassName = helper.cls_name(test)
            if not self.failures:
                self.stream.writeln()
                self.stream.writeln(Fore.RESET + "Thinking {0}".format(helper.cls_name(test)))

    def addSuccess(self, test):
        if self.passesCount():            
            MockableTestResult.addSuccess(self, test)
            self.stream.writeln(Fore.GREEN + "  {0} has expanded your"
                                             "awareness.".format(test._testMethodName))
            self.pass_count += 1

    def addError(self, test, err):
        # Having 1 list for errors and 1 list for failures would mess with
        # the error sequence
        self.addFailure(test, err)

    def passesCount(self):
        return not (self.failures and helper.cls_name(self.failures[0][0]) != self.prevTestClassName)
        
    def addFailure(self, test, err):
        MockableTestResult.addFailure(self, test, err)

    def sortFailures(self, testClassName):
        table = list()
        for test, err in self.failures:
            if helper.cls_name(test) ==  testClassName:
                m = re.search("(?<= line )\d+" ,err)
                if m:
                    tup = (int(m.group(0)), test, err)
                    table.append(tup)
               
        if table:
            return sorted(table)
        else:
            return None
         
    def firstFailure(self):
        if not self.failures: return None
        
        table = self.sortFailures(helper.cls_name(self.failures[0][0]))
            
        if table:
            return (table[0][1], table[0][2])
        else:
            return None
    
    def learn(self):
        self.errorReport()
    
        self.stream.writeln("")
        self.stream.writeln("")
        self.stream.writeln(self.say_something_zenlike())
        
        if self.failures: return
        self.stream.writeln("\n**************************************************")
        self.stream.writeln("That was the last one, well done!")
        self.stream.writeln("\nIf you want more, take a look at about_extra_credit_task.py")
        
    def errorReport(self):
        problem = self.firstFailure()
        if not problem: return 
        test, err = problem 
        self.stream.writeln(Fore.RED + "  {0} has damaged your"
                                       "karma.".format(test._testMethodName))        

        self.stream.writeln("")
        self.stream.writeln(Fore.RESET + "You have not yet reached enlightenment ...")
        self.stream.writeln(Fore.RED + ""
                                       "{0}".format(self.scrapeAssertionError(err)))
        self.stream.writeln("")
        self.stream.writeln(Fore.RESET + "Please meditate on the following code:")
        self.stream.writeln(Fore.YELLOW +
                           (self.scrapeInterestingStackDump(err)))

    def scrapeAssertionError(self, err):
        if not err: return ""

        error_text = ""
        count = 0
        for line in err.splitlines():
            m = re.search("^[^^ ].*$",line)
            if m and m.group(0):
                count+=1
            
            if count>1:
                error_text += ("  " + line.strip()).rstrip() + '\n'
        return error_text.strip('\n')

    def scrapeInterestingStackDump(self, err):
        if not err:
            return ""

        lines = err.splitlines()
        
        sep = '@@@@@SEP@@@@@'
        
        scrape = ""
        for line in lines:
            m = re.search("^  File .*$",line)
            if m and m.group(0):
                scrape += '\n' + line

            m = re.search("^    \w(\w)+.*$",line)
            if m and m.group(0):
                scrape += sep + line
            
        lines = scrape.splitlines()
                        
        scrape = ""
        for line in lines:
            m = re.search("^.*[/\\\\]koans[/\\\\].*$",line)
            if m and m.group(0):
                scrape += line + '\n'
        return scrape.replace(sep, '\n').strip('\n')

    # Hat's tip to Tim Peters for the zen statements from The Zen
    # of Python (http://www.python.org/dev/peps/pep-0020/)
    #
    # Also a hat's tip to Ara T. Howard for the zen statements from his
    # metakoans Ruby Quiz (http://rubyquiz.com/quiz67.html) and
    # Edgecase's later permatation in the Ruby Koans
    def say_something_zenlike(self):
        if self.failures:
            turn = self.pass_count % 37

            if turn == 0:            
                return Fore.CYAN + "Beautiful is better than ugly."
            elif turn == 1 or turn == 2:
                return Fore.CYAN + "Explicit is better than implicit."
            elif turn == 3 or turn == 4:
                return Fore.CYAN + "Simple is better than complex."
            elif turn == 5 or turn == 6:
                return Fore.CYAN + "Complex is better than complicated."
            elif turn == 7 or turn == 8:
                return Fore.CYAN + "Flat is better than nested."
            elif turn == 9 or turn == 10:
                return Fore.CYAN + "Sparse is better than dense."
            elif turn == 11 or turn == 12:
                return Fore.CYAN + "Readability counts."
            elif turn == 13 or turn == 14:
                return Fore.CYAN + ("Special cases aren't special enough to"
                                    "break the rules.")
            elif turn == 15 or turn == 16:
                return Fore.CYAN + "Although practicality beats purity."
            elif turn == 17 or turn == 18:
                return Fore.CYAN + "Errors should never pass silently."
            elif turn == 19 or turn == 20:
                return Fore.CYAN + "Unless explicitly silenced."
            elif turn == 21 or turn == 22:
                return Fore.CYAN + ("In the face of ambiguity, refuse the"
                                    "temptation to guess.")
            elif turn == 23 or turn == 24:
                return Fore.CYAN + ("There should be one-- and preferably only"
                                    "one --obvious way to do it.")
            elif turn == 25 or turn == 26:
                return Fore.CYAN + ("Although that way may not be obvious at"
                                    "first unless you're Dutch.")
            elif turn == 27 or turn == 28:
                return Fore.CYAN + "Now is better than never."
            elif turn == 29 or turn == 30:
                return Fore.CYAN + ("Although never is often better than right"
                                    "now.")
            elif turn == 31 or turn == 32:
                return Fore.CYAN + ("If the implementation is hard to explain,"
                                    "it's a bad idea.")
            elif turn == 33 or turn == 34:
                return Fore.CYAN + ("If the implementation is easy to explain,"
                                    "it may be a good idea.")
            else: 
                return Fore.CYAN + ("Namespaces are one honking great idea --"
                                    "let's do more of those!")
        
        else:
            return Fore.BLUE + "Nobody ever expects the Spanish Inquisition."
        
        # Hopefully this will never ever happen!
        return "The temple in collapsing! Run!!!"
    