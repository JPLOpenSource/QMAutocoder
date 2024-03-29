#!/bin/env python3
# -----------------------------------------------------------------------
# fprimetemplates.py
#
# A python class that contains template code for the QMAutocoder 
# fprime back-end 
#
# -----------------------------------------------------------------------

from Cheetah.Template import Template # type: ignore
from typing import List, Dict, Tuple, Any, Optional, IO

class FprimeTemplate:
    
# -------------------------------------------------------------------------------
# target
# -------------------------------------------------------------------------------   
        def target(self, targ: str) -> str:
            
            template = Template("""this->state = $(target);""")
                     
            template.target = targ
            return str(template)
        
# -------------------------------------------------------------------------------
# ifGuard
# ------------------------------------------------------------------------------- 
        def ifGuard(self, smname: str, action: str, args: str) -> str:  
            if args == "":
                template = Template("""if ( parent->$(smname)_$(action)() ) {""")
            else:
                template = Template("""if (parent->$(smname)_$(action)($(args)) ) {""")       

            template.smname = smname
            template.action = action
            template.args = args
            return str(template)  


# -------------------------------------------------------------------------------
# guardSignature
# -------------------------------------------------------------------------------   
        def guardSignature(self, smname: str, action: str, args: str) -> str:
            if args == "":
                template = Template("""bool $(smname)_$(action)()""")
            elif args == "e":
                template = Template("""bool $(smname)_$(action)(const Svc::SMEvents *e)""")
            elif args.isdigit():
                template = Template("""bool $(smname)_$(action)(int arg)""")
            else:
                assert True, "Unknown args"


            template.smname = smname
            template.action = action
            return str(template)

# -------------------------------------------------------------------------------
# guardDef
# -------------------------------------------------------------------------------   
        def guardDef(self, smname: str, action: str, component: str, args: str, namespace) -> str:
            if args == "":
                template = Template("""bool $(namespace)::$(component)::$(smname)_$(action)()""")
            elif args == "e":
                template = Template("""bool $($namespace)::$(component)::$(smname)_$(action)(const Svc::SMEvents *e)""")
            elif args.isdigit():
                template = Template("""bool $(namespace)::$(component)::$(smname)_$(action)(int arg)""")
            else:
                assert True, "Unknown args"

            template.smname = smname
            template.namespace = namespace
            template.action = action
            template.component = component
            return str(template)

# -------------------------------------------------------------------------------
# action
# -------------------------------------------------------------------------------   
        def action(self, smname: str, action: str, args: str) -> str:
            if args == "":
                template = Template("""parent->$(smname)_$(action)();""")   
            else:
                template = Template("""parent->$(smname)_$(action)($(args));""")         
     
            template.smname = smname
            template.action = action
            template.args = args
            return str(template)


# -------------------------------------------------------------------------------
# actionSignature
# -------------------------------------------------------------------------------   
        def actionSignature(self, smname: str, action: str, args: str) -> str:
            if args == "":
                template = Template("""void $(smname)_$(action)()""")
            elif args == "e":
                template = Template("""void $(smname)_$(action)(const Svc::SMEvents *e)""")
            elif args.isdigit():
                template = Template("""void $(smname)_$(action)(int arg)""")
            else:
                assert True, "Unknown args"


            template.smname = smname
            template.action = action
            return str(template)


# -------------------------------------------------------------------------------
# actionDef
# -------------------------------------------------------------------------------   
        def actionDef(self, smname: str, action: str, component: str, args: str, namespace: str) -> str:
            if args == "":
                template = Template("""void $(namespace)::$(component)::$(smname)_$(action)()""")   
            elif args == "e":
                template = Template("""void $(namespace)::$(component)::$(smname)_$(action)(const Svc::SMEvents *e)""")         
            elif args.isdigit():
                template = Template("""void $(namespace)::$(component)::$(smname)_$(action)(int arg)""")         
            else:
                assert True, "Unknown args"
                
            template.namespace = namespace
            template.smname = smname
            template.action = action
            template.component = component
            return str(template)

# -------------------------------------------------------------------------------
# stateTransition
# -------------------------------------------------------------------------------   
        def stateTransition(self, signal: str, transition: str) -> str:
            template = Template("""
                case $(signal):
$(transition)
                    break;
    """)
            template.signal = signal
            template.transition = transition
            return str(template)
        
        
# -------------------------------------------------------------------------------
# fileHeader
# -------------------------------------------------------------------------------   
        def fileHeader(self, smname: str, stateList: List[str], eventList: List[str], namespace: str, implFunctions: List[str]) -> str:
            template  = Template("""
// ======================================================================
// \\title  $(smname).h
// \\author Auto-generated
// \\brief  header file for state machine $smname
//
// \\copyright
// Copyright 2009-2015, by the California Institute of Technology.
// ALL RIGHTS RESERVED.  United States Government Sponsorship
// acknowledged.
//
// ======================================================================
           
#ifndef $(smname.upper())_H_
#define $(smname.upper())_H_

namespace Svc {
  class SMEvents;
}

namespace $(namespace) {

class $(smname)If {
  public:
    #for $function in $implFunctions
    virtual $function = 0;
    #end for
                                                                  
};

class $(smname) {
                                 
  private:
    $(smname)If *parent;
                                 
  public:
                                 
    $(smname)($(smname)If* parent) : parent(parent) {}
  
    enum $(smname)States {
#for $state in $stateList
      $state,
#end for
    };

    enum $(smname)Events {
#for $event in $eventList
      $event,
#end for
    };
    
    enum $(smname)States state;

    void * extension;

    void init();
    void update(const Svc::SMEvents *e);

};

}

#endif
""") 
            template.stateList = stateList
            template.eventList = eventList
            template.smname = smname
            template.namespace = namespace
            template.implFunctions = implFunctions
            return str(template)
        
        
        
# -------------------------------------------------------------------------------
# stateMachineInit
# -------------------------------------------------------------------------------           
        def stateMachineInit(self, smname: str, transition: str, namespace: str) -> str:
            template = Template("""
// ======================================================================
// \\title  $(smname).cpp
// \\author Auto-generated
// \\brief  cpp file for state machine $smname
//
// \\copyright
// Copyright 2009-2015, by the California Institute of Technology.
// ALL RIGHTS RESERVED.  United States Government Sponsorship
// acknowledged.
//
// ======================================================================            
    
\#include "stdio.h"
\#include "assert.h"
\#include "SMEvents.hpp"
\#include "$(smname).h"


void $(namespace)::$(smname)::init()
{
$transition
}


void $(namespace)::$(smname)::update(const Svc::SMEvents *e)
{
    switch (this->state) {
    """)
            template.smname = smname
            template.transition = transition
            template.namespace = namespace
            return str(template)
        

# -------------------------------------------------------------------------------
# stateMachineState
# -------------------------------------------------------------------------------     
        def stateMachineState(self, state: str) -> str:
            template = Template("""
            /**
            * state $state
            */
            case $state:
            
            switch (e->geteventSignal()) {
""")
            template.state = state
            return str(template)
        
        
# -------------------------------------------------------------------------------
# stateMachineBreak
# -------------------------------------------------------------------------------       
        def stateMachineBreak(self) -> str:
            template = Template("""
                default:
                    break;
            }
            break;
    """)  
            return str(template)
        
        
# -------------------------------------------------------------------------------
# stateMachineFinalBreak
# -------------------------------------------------------------------------------   
        def stateMachineFinalBreak(self) -> str:
            template = Template("""
        default:
        assert(0);
    }
}
""")
            return str(template)

