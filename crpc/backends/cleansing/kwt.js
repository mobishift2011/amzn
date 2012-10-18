// requires
var utils = require('utils');
var f = utils.format;
var casper = require('casper').create({
    verbose: false,
    logLevel: "error"
});

// monkey patching
casper.checkStep = function checkStep(self, onComplete) {
    if (self.pendingWait || self.loadInProgress) {
        return;
    }
    self.current = self.step;                 // Added:  New Property.  self.current is current execution step pointer
    var step = self.steps[self.step++];
    if (utils.isFunction(step)) {
        self.runStep(step);
        step.executed = true;                 // Added:  This navigation step is executed already or not.
    } else {
        self.result.time = new Date().getTime() - self.startTime;
        self.log(f("Done %s steps in %dms", self.steps.length, self.result.time), "info");
        clearInterval(self.checker);
        self.emit('run.complete');
        if (utils.isFunction(onComplete)) {
            try {
                onComplete.call(self, self);
            } catch (err) {
                self.log("Could not complete final step: " + err, "error");
            }
        } else {
            // default behavior is to exit
            self.exit();
        }
    }
};

casper.then = function then(step) {
    if (!this.started) {
        throw new CasperError("Casper not started; please use Casper#start");
    }
    if (!utils.isFunction(step)) {
        throw new CasperError("You can only define a step as a function");
    }
    // check if casper is running
    if (this.checker === null) {
        // append step to the end of the queue
        step.level = 0;
        this.steps.push(step);
        step.executed = false;                 // Added:  New Property. This navigation step is executed already or not.
        this.emit('step.added', step);         // Moved:  from bottom
    } else {

      if( !this.steps[this.current].executed ) {  // Added:  Add step to this.steps only in the case of not being executed yet.
        // insert substep a level deeper
        try {
//          step.level = this.steps[this.step - 1].level + 1;   <=== Original
            step.level = this.steps[this.current].level + 1;   // Changed:  (this.step-1) is not always current navigation step
        } catch (e) {
            step.level = 0;
        }
        var insertIndex = this.step;
        while (this.steps[insertIndex] && step.level === this.steps[insertIndex].level) {
            insertIndex++;
        }
        this.steps.splice(insertIndex, 0, step);
        step.executed = false;                    // Added:  New Property. This navigation step is executed already or not.
        this.emit('step.added', step);            // Moved:  from bottom
      }                                           // Added:  End of if() that is added.

    }
//    this.emit('step.added', step);   // Move above. Because then() is not always adding step. only first execution time.
    return this;
};

casper.label = function label( labelname ) {
  var step = new Function('"empty function for label: ' + labelname + ' "');   // make empty step
  step.label = labelname;                                 // Adds new property 'label' to the step for label naming
  this.then(step);                                        // Adds new step by then()
};

casper.goto = function goto( labelname ) {
  for( var i=0; i<this.steps.length; i++ ){         // Search for label in steps array
      if( this.steps[i].label == labelname ) {      // found?
        this.step = i;                              // new step pointer is set
      }
  }
};

casper.dumpSteps = function dumpSteps( showSource ) {
  this.echo( "=========================== Dump Navigation Steps ==============================", "RED_BAR");
  if( this.current ){ this.echo( "Current step No. = " + (this.current+1) , "INFO"); }
  this.echo( "Next    step No. = " + (this.step+1) , "INFO");
  this.echo( "steps.length = " + this.steps.length , "INFO");
  this.echo( "================================================================================", "WARNING" );

  for( var i=0; i<this.steps.length; i++){
    var step  = this.steps[i];
    var msg   = "Step: " + (i+1) + "/" + this.steps.length + "     level: " + step.level
    if( step.executed ){ msg = msg + "     executed: " + step.executed }
    var color = "PARAMETER";
    if( step.label    ){ color="INFO"; msg = msg + "     label: " + step.label }

    if( i == this.current ) {
      this.echo( msg + "     <====== Current Navigation Step.", "COMMENT");
    } else {
      this.echo( msg, color );
    }
    if( showSource ) {
      this.echo( "--------------------------------------------------------------------------------" );
      this.echo( this.steps[i] );
      this.echo( "================================================================================", "WARNING" );
    }
  }
};

// setup globals 
var email = casper.cli.options['email'] || 'kwtools3456@gmail.com';
var passwd = casper.cli.options['passwd'] || '1qaz2wsx!@';
var keywords = casper.cli.options['keywords'] || 'iphone,cars,kindle';
keywords = keywords.split(',');

var kwurl = ''
var result = {}
var kws_list = [];
for (var j=0; j<((keywords.length-1)/50+1); j++) {
    kws_list.push( keywords.slice(j*50, j*50+50) );
}

// login & save url 
casper.start('http://adwords.google.com');

casper.thenEvaluate(function login(email, passwd) {
    document.querySelector('#Email').setAttribute('value', email);
    document.querySelector('#Passwd').setAttribute('value', passwd);
    document.querySelector('form').submit();
}, {email:email, passwd:passwd});

casper.waitForSelector(".aw-cues-item");

casper.then(function(){
    kwurl = this.evaluate(function(){
        var search = document.location.search;
        return 'https://adwords.google.com/o/Targeting/Explorer'+search+'&__o=cues&ideaRequestType=KEYWORD_IDEAS';
    })
});

casper.then(function(){
    this.open(kwurl);
});

casper.waitForSelector("button.gwt-Button");


// control flows 
var current_kws = 0;
casper.label("LOOP_START");
    casper.then(function(){
        var kws = kws_list[current_kws];
        this.evaluate(function(kws){
            document.querySelector('.sEAB').value = kws.join('\n');
            document.querySelector('button.gwt-Button').click();
        }, {kws:kws});
    });

    //casper.waitForSelector("a.sCM");
    casper.waitFor(function(){
        var kws = kws_list[current_kws];
        return this.evaluate(function(kws){
            var els = document.querySelectorAll('a.sCM');
            for (var i=0; i<els.length; i++){
                if (els[i].textContent == kws[0]){
                    return true
                }
            }
            return false
        }, {kws:kws})
    }, then=null, onTimeout=function(){
        // if we encoutner an timeout, skip it
        utils.dump(result);
        this.exit();
    }, timeout=1500);

    casper.then(function() {
        var o = this.evaluate(function(){ 
            var o = {};
            var els = document.querySelectorAll('a.sCM');
            for (var i=0; i<els.length; i++){
                var el = els[i];
                pel = el.parentElement.parentElement.parentElement.parentElement.parentElement;
                o[el.textContent] = [pel.nextSibling.nextSibling.textContent, pel.nextSibling.nextSibling.nextSibling.textContent];
            };
            return o
        });
        for (var k in o){
            result[k] = o[k];
        }
    });

    casper.then(function(){
        current_kws++;
        if (kws_list[current_kws] && kws_list[current_kws].length>0){
            this.goto("LOOP_START");
        }
    });

casper.run(function(){
    utils.dump(result);
    this.exit();
})
