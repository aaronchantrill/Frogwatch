#!/usr/bin/env python2
# -*- coding: utf-8 -*-
from datetime import datetime
import json
import re
import urlparse
from urllib2 import unquote
import os, random, sys

import cgitb
cgitb.enable()

# Declare my list of frogs as a global variable
frogs = [
    ['AmericanBullfrog','American Bullfrog'],
    ['BarkingTreefrog','Barking Treefrog'],
    ['BrimleysChorusFrog',"Brimley's Chorus Frog"],
    ['CopesGrayTreefrog',"Cope's Gray Treefrog"],
    ['EasternAmericanToad',"Eastern American Toad"],
    ['EasternNarrow-mouthToad',"Eastern Narrow-mouthed Toad"],
    ['EasternSpadefoot',"Eastern Spadefoot"],
    ['FowlersToad',"Fowler's Toad"],
    ['GrayTreefrog',"Gray Treefrog"],
    ['GreenFrog',"Green Frog"],
    ['GreenTreefrog',"Green Treefrog"],
    ['NorthernCricketFrog',"Northern Cricket Frog"],
    ['PickerelFrog',"Pickerel Frog"],
    ['PineWoodsTreefrog',"Pine Woods Treefrog"],
    ['SouthernCricketFrog',"Southern Cricket Frog"],
    ['SouthernLeopardFrog',"Southern Leopard Frog"],
    ['SouthernToad',"Southern Toad"],
    ['SpringPeeper',"Spring Peeper"],
    ['UplandChorusFrog',"Upland Chorus Frog"]
]

# Set a number of frogs to select from
# path to the audio files
filepath = "/home/drask/Documents/Frogwatch/8bit_mono"
reQS=re.compile("([^=]+)=([^&]*)&?")

def wavurl(filename):
    return "/Frogwatch/{}.wav".format(filename)

def imgurl(filename):
    return "/Frogwatch/{}.jpg".format(filename)

def application(environ,start_response):
    wavfile=""
    imgfile=""
    correct="0"
    incorrect="0"
    ret=[]
    answer_count = 2
    working_frogs = frogs
    '''
    if( environ["PATH_INFO"]=="/favicon.ico" ):
        print("Content-Type: text/plain;charset=utf-8")
        print("")
        #start_response('404 Not Found',[('content-type','text/plain;charset=utf-8')])
        ret="404 Not Found"
        return ret
    else:
    '''
    if True:
        showImages=True
        skip=[]
        # gather parameters from GET
        if( "QUERY_STRING" in environ ):
            for namevalue in reQS.findall(environ["QUERY_STRING"]):
                if( namevalue[0].lower()=="wavfile" ):
                    wavfile="{}/{}.wav".format(filepath,namevalue[1])
                if( namevalue[0].lower()=="imgfile" ):
                    imgfile="{}/{}.jpg".format(filepath,namevalue[1])
                if( namevalue[0].lower()=="correct" ):
                    correct=namevalue[1]
                if( namevalue[0].lower()=="incorrect" ):
                    incorrect=namevalue[1]
                if( namevalue[0].lower()=="choices" ):
                    try:
                        answer_count=int(namevalue[1])
                    except ValueError:
                        pass
                if( namevalue[0].lower()=="hideimages"):
                    if(namevalue[1]=="1"):
                        showImages=False
                if( namevalue[0].lower()=="resetscore"):
                    correct="0"
                    incorrect="0"
                if( namevalue[0].lower()=="skip"):
                    for skipped in namevalue[1].split('%2C'):
                        skip.append(skipped)
                        working_frogs=list(filter(lambda frog:frog[0]!=skipped,working_frogs))

        if(answer_count>len(working_frogs)):
            answer_count=len(working_frogs)
        # gather parameters from POST
        content_length=0
        if( "CONTENT_LENGTH" in environ ):
            content_length = int(environ['CONTENT_LENGTH'])
            post_data=environ['wsgi.input'].read(content_length)
            # Parse it out
            for namevalue in reQS.findall(post_data):
                print("posted: {}={}".format(namevalue[0].namevalue[1]))

        if( len(wavfile) and os.path.isfile(wavfile) ):
            #start_response('200 OK',[('content-type','audio/wav')])
            print('Content-type: audio/wav')
            print('')
            with open(wavfile, "rb") as w:
                ret = w.read()
            return ret
        elif( len(imgfile) and os.path.isfile(imgfile) ):
            #start_response('200 OK',[('content-type','image/jpeg')])
            print('Content-type: image/jpeg')
            print('')
            with open(imgfile, "rb") as w:
                ret = w.read()
            return ret
        else:
            # Create a list from 0 to 18 to hold my list of frogs
            frog_list = range(len(working_frogs))
            random.shuffle(frog_list)
            # Get our list of possible answers
            frog_list=frog_list[:answer_count]
            # Set the answer to a random element
            answer = frog_list[random.randint(0,answer_count-1)]
            # print pictures of each possible frog answer, with the
            # frog name below.
            ret=[]
            #start_response('200 OK',[('content-type','text/html;charset=utf-8')])
            print("Content-type: text/html")
            print("")
            ret.append("""
<!DOCTYPE html>
<html lang="en-US">
<head>
<title>Test</title>
<meta charset="utf-8"/>
<style type="text/css">
 /* Style the tab */
.tab {
  overflow: hidden;
  border: 1px solid #ccc;
  background-color: #f1f1f1;
}

/* Style the buttons that are used to open the tab content */
.tab button {
  background-color: inherit;
  float: left;
  border: none;
  outline: none;
  cursor: pointer;
  padding: 14px 16px;
  transition: 0.3s;
}

/* Change background color of buttons on hover */
.tab button:hover {
  background-color: #ddd;
}

/* Create an active/current tablink class */
.tab button.active {
  background-color: #ccc;
}

/* Style the tab content */
.tabcontent {
  display: none;
  padding: 6px 12px;
  border: 1px solid #ccc;
  border-top: none;
} 
.tabcontent.active {
  display: block;
}
.selection{
  border:1px solid #000;
  float: left;
  cursor: pointer;
}
</style>
<script type="text/javascript">
    correct = """+str(correct)+""";
    incorrect = """+str(incorrect)+""";
    function checkanswer(answer){
        // stop any active playback
        stopall();
        if(answer=="""+str(answer)+"""){
            correct++;
            document.getElementById("options_correct").value=correct;
            document.getElementById("correct").innerHTML=correct;
            alert("Correct!");
            //activate the next button
            next();
        }else{
            incorrect++;
            document.getElementById("options_incorrect").value=incorrect;
            document.getElementById("incorrect").innerHTML=incorrect;
            document.getElementById("frog"+answer).play();
            alert("Sorry, that's not correct. Here is what that frog does sound like.");
        }
    }
    function stopall(el){
        audioplayers=document.getElementsByTagName("audio");
        for(i=0;i<audioplayers.length;++i){
            if(audioplayers[i]!=el){
                audioplayers[i].pause();
                audioplayers[i].currentTime=0;
            }
        }
    }
    function next(){
        document.getElementById("optionsform").submit();
    }
    function openTab(evt, tabName) {
        // Declare all variables
        var i, tabcontent, tablinks;

        // Get all elements with class="tabcontent" and hide them
        tabcontent = document.getElementsByClassName("tabcontent");
        for (i = 0; i < tabcontent.length; i++) {
            tabcontent[i].className = "tabcontent";
        }

        // Get all elements with class="tablinks" and remove the class "active"
        tablinks = document.getElementsByClassName("tablinks");
        for (i = 0; i < tablinks.length; i++) {
            tablinks[i].className = tablinks[i].className.replace(" active", "");
        }

        // Show the current tab, and add an "active" class to the button that opened the tab
        document.getElementById(tabName).className = "tabcontent active";
        evt.currentTarget.className += " active";
    }
    function hideImages(checked){
        if(checked){
            document.getElementById("options_hideimages").value="0";
        }else{
            document.getElementById("options_hideimages").value="1";
        }
    }
    function setskip(el){
        var noskip=document.getElementsByClassName("noskip");
        var skip=new Array();
        unskipped=0;
        for(i=0;i<noskip.length;++i){
            if(!noskip[i].checked){
                skip[skip.length]=noskip[i].value;
            }else{
                unskipped+=1;
            }
        }
        if(unskipped<2){
            el.checked=true;
            alert("You must leave at least 2 options");
        }else{
            document.getElementById("options_skip").value=skip.join(",");
        }
    }
</script>
</head>
<body>
"""
            )
            ret.append("""
<!-- Tab links -->
<div class="tab">
  <button class="tablinks active" onclick="openTab(event, 'Game')">Game</button>
  <button class="tablinks" onclick="openTab(event, 'Options')">Options</button>
</div>
<!-- Tab content -->
<div id="Game" class="tabcontent active">
<h1>Correct: <span id="correct">"""+correct+"""</span> Incorrect: <span id="incorrect">"""+incorrect+'''</span></h1>
<audio controls="controls" type="audio/wav" onplay="stopall(this);"><source src="'''+wavurl(working_frogs[answer][0])+'''" /></audio>
<div style="clear:both;">
<form id="topform" name="top"><input type="button" onclick="next()" value="Next"/></form>
</div>
'''
            )
            for frog in frog_list:
                ret.append('''
<div class="selection" onclick="checkanswer({frog})">
'''.format(frog=frog)
                )
                if(showImages):
                    ret.append('''
<img src="{imgfile}"/>
'''.format(imgfile=imgurl(working_frogs[frog][0]))
                    )
                ret.append('''
<h2>{frogname}</h2>
<audio id="frog{frog}" type="audio/wav"><source src="{wavfile}"/></audio>
</div>'''.format(frog=frog, wavfile=wavurl(working_frogs[frog][0]), frogname=working_frogs[frog][1])
                )
            ret.append("""
<div style="clear:both;">
<form id="bottomform" name="bottom"><input type="button" onclick="next()" value="Next"/></form>
</div>
</div><!-- Game -->
<!-- Tab content -->
<div id="Options" class="tabcontent">
<form id="optionsform" name="options">
Give me <select name="choices">""")
            for i in range(2,len(frogs)+1):
                ret.append('<option value="{}" {}>{}</option>'.format(i,"selected" if i==answer_count else "",i))
            ret.append('''
</select> options to choose from<br />
<input type="hidden" id="options_correct" name="correct" value="'''+str(correct)+'''"/>
<input type="hidden" id="options_incorrect" name="incorrect" value="'''+str(incorrect)+'''"/>
<input type="hidden" id="options_hideimages" name="hideimages" value="'''+('0' if showImages else '1')+'''"/>
<input type="checkbox" id="options_showimages" name="showimages" '''+('checked="checked" ' if showImages else '')+'''onchange="hideImages(this.checked)"/> <label for="options_showimages">Show Images</label><br />
<input type="checkbox" id="options_resetScore" name="resetScore" value='1'/> <label for="options_resetScore">Reset Score</label><br />
<input type="hidden" id="options_skip" name="skip" value="'''+','.join(skip)+'''">
Test on the following:<br />
'''
            )
            for frog in frogs:
                ret.append(
                    '<input type="checkbox" class="noskip" id="options_{frog}" value="{frog}" onchange="setskip(this)" {checked}> {frogname}<br />'.format(
                        frog=frog[0],
                        frogname=frog[1],
                        checked=('' if frog[0] in skip else 'checked="checked"')
                    )
                )
            ret.append('''
<input type="submit" value="Submit"/>
</form>
</div><!-- Options -->
<div style="text-align: center;font-family: san-serif; font-size: smaller;">
Images and audio clips &copy; 2019 Copyright <a href="https://www.virginiaherpetologicalsociety.com/">Virginia Herpetological Society</a>. All Rights Reserved
</div>
</body>
</html>
'''
            )
    return ret
if __name__ == "__main__":
    response = application(os.environ,None)
    print("\n".join(response))
