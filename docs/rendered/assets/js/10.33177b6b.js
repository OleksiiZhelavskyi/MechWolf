(window.webpackJsonp=window.webpackJsonp||[]).push([[10],{190:function(e,t,n){"use strict";n.r(t);var a=n(0),r=Object(a.a)({},function(){var e=this,t=e.$createElement,n=e._self._c||t;return n("ContentSlotsDistributor",{attrs:{"slot-key":e.$parent.slotKey}},[n("h1",{attrs:{id:"a-very-gentle-introduction"}},[n("a",{staticClass:"header-anchor",attrs:{href:"#a-very-gentle-introduction","aria-hidden":"true"}},[e._v("#")]),e._v(" A "),n("em",[e._v("Very")]),e._v(" Gentle Introduction")]),e._v(" "),n("h2",{attrs:{id:"an-introduction-to-the-introduction"}},[n("a",{staticClass:"header-anchor",attrs:{href:"#an-introduction-to-the-introduction","aria-hidden":"true"}},[e._v("#")]),e._v(" An Introduction to the Introduction")]),e._v(" "),n("p",[e._v("This gentle introduction is made for people with "),n("strong",[e._v("absolutely no coding\nexperience")]),e._v(" who are likely feeling very lost right now. To tell if this\nguide is right for you, if you know what the command "),n("code",[e._v("pip install XXXXX")]),e._v("\ndoes, then feel free to skip this section. If not, welcome! We'll cover\nthe background knowledge you'll need for the general "),n("a",{attrs:{href:"./getting_started"}},[e._v("getting started guide")]),e._v(".")]),e._v(" "),n("h2",{attrs:{id:"learn-python"}},[n("a",{staticClass:"header-anchor",attrs:{href:"#learn-python","aria-hidden":"true"}},[e._v("#")]),e._v(" Learn Python")]),e._v(" "),n("p",[e._v("MechWolf is written in Python, a high level programming language that is\nthe "),n("em",[e._v("lingua franca")]),e._v(" of scientific computation. This one language can do\nanything from "),n("a",{attrs:{href:"http://keras.io",target:"_blank",rel:"noopener noreferrer"}},[e._v("machine learning"),n("OutboundLink")],1),e._v(" to "),n("a",{attrs:{href:"http://flask.pocoo.org",target:"_blank",rel:"noopener noreferrer"}},[e._v("web server\ndevelopment"),n("OutboundLink")],1),e._v(" and now flow process automation. In\norder to get started with MechWolf, you'll need to learn Python,\nspecifically Python 3.")]),e._v(" "),n("p",[n("a",{attrs:{href:"https://en.wikipedia.org/wiki/Phrases_from_The_Hitchhiker%27s_Guide_to_the_Galaxy#Don't_Panic",target:"_blank",rel:"noopener noreferrer"}},[e._v("Don't panic."),n("OutboundLink")],1)]),e._v(" "),n("p",[e._v("You can pick up the basics of Python in a day or two. A few good\nresources are listed here:")]),e._v(" "),n("ul",[n("li",[n("a",{attrs:{href:"https://www.codecademy.com/learn/learn-python",target:"_blank",rel:"noopener noreferrer"}},[e._v("Codecademy"),n("OutboundLink")],1)]),e._v(" "),n("li",[n("a",{attrs:{href:"https://docs.python.org/3/tutorial/index.html",target:"_blank",rel:"noopener noreferrer"}},[e._v("The official Python\ntutorial"),n("OutboundLink")],1)]),e._v(" "),n("li",[n("a",{attrs:{href:"https://learnpythonthehardway.org/python3/",target:"_blank",rel:"noopener noreferrer"}},[e._v("Learn Python the Hard\nWay"),n("OutboundLink")],1),e._v(" (note: despite the\nname, it isn't actually hard)")])]),e._v(" "),n("h2",{attrs:{id:"install-python-3-7-or-greater"}},[n("a",{staticClass:"header-anchor",attrs:{href:"#install-python-3-7-or-greater","aria-hidden":"true"}},[e._v("#")]),e._v(" Install Python 3.7 or greater")]),e._v(" "),n("p",[e._v("Although Python is likely already installed on your computer (especially\nif you're using Mac or Linux), you probably don't have a recent enough\nversion of Python to support MechWolf. Python is available from the\n"),n("a",{attrs:{href:"https://www.python.org/downloads/",target:"_blank",rel:"noopener noreferrer"}},[e._v("download page at Python.org"),n("OutboundLink")],1),e._v(". For a\ndetailed guide, see "),n("a",{attrs:{href:"http://docs.python-guide.org/en/latest/starting/installation/",target:"_blank",rel:"noopener noreferrer"}},[e._v("The Hitchhiker's Guide to Python section on\ninstalling\nPython 3"),n("OutboundLink")],1),e._v(".")]),e._v(" "),n("div",{staticClass:"warning custom-block"},[n("p",{staticClass:"custom-block-title"},[e._v("WARNING")]),e._v(" "),n("p",[e._v("Be sure to download Python 3.7! MechWolf is written in Python 3, which is\nnot backwards compatible.")])]),e._v(" "),n("h2",{attrs:{id:"learn-the-command-line"}},[n("a",{staticClass:"header-anchor",attrs:{href:"#learn-the-command-line","aria-hidden":"true"}},[e._v("#")]),e._v(" Learn the Command Line")]),e._v(" "),n("p",[e._v("In order to effectively use your computer to code, you'll want to\nunderstand how to use the command line, at least to a cursory level. Go\nover "),n("a",{attrs:{href:"https://www.codecademy.com/articles/command-line-commands",target:"_blank",rel:"noopener noreferrer"}},[e._v("common\ncommands"),n("OutboundLink")],1),e._v(" to\nat least get an idea of how to navigate the filesystem ("),n("code",[e._v("cd")]),e._v(", "),n("code",[e._v("ls")]),e._v(", and\n"),n("code",[e._v("pwd")]),e._v("). This will be invaluable going forward.")]),e._v(" "),n("h2",{attrs:{id:"create-a-virtualenv-optional"}},[n("a",{staticClass:"header-anchor",attrs:{href:"#create-a-virtualenv-optional","aria-hidden":"true"}},[e._v("#")]),e._v(" Create a virtualenv "),n("em",[e._v("(optional)")]),e._v(" "),n("a",{attrs:{id:"virtualenv"}})]),e._v(" "),n("p",[n("a",{attrs:{href:"https://virtualenv.pypa.io/en/stable/",target:"_blank",rel:"noopener noreferrer"}},[e._v("virtualenv"),n("OutboundLink")],1),e._v(" is a tool that\nallows you to create isolated environments on your computer. For\nexample, imagine that one piece of code required having version 1.0 of\nMechWolf but another required version 2.0. The solution is to run each\npiece of code inside a virtual environment to keep their dependencies\nseparate. You don't have to do this step, but it's "),n("strong",[e._v("highly\nrecommended")]),e._v(" to prevent bad, unpredictable things from happening that\ncan be hard to debug. "),n("a",{attrs:{href:"http://docs.python-guide.org/en/latest/dev/virtualenvs/#lower-level-virtualenv",target:"_blank",rel:"noopener noreferrer"}},[e._v("The Hitchhiker's Guide to Python's section on\nvirtualenv"),n("OutboundLink")],1),e._v("\nis well worth the read for getting a feel for virtualenv.")]),e._v(" "),n("p",[e._v("To install virtualenv use the following command in your terminal:")]),e._v(" "),n("div",{staticClass:"language-bash extra-class"},[n("pre",{pre:!0,attrs:{class:"language-bash"}},[n("code",[e._v("$ pip3 "),n("span",{pre:!0,attrs:{class:"token function"}},[e._v("install")]),e._v(" virtualenv\n")])])]),n("p",[e._v("Then in the directory you want to use, create a virtualenv named\nmechwolf-env:")]),e._v(" "),n("div",{staticClass:"language-bash extra-class"},[n("pre",{pre:!0,attrs:{class:"language-bash"}},[n("code",[e._v("$ virtualenv -p python3.7 mechwolf-env\n")])])]),n("p",[e._v("And then activate the environment with:")]),e._v(" "),n("div",{staticClass:"language-bash extra-class"},[n("pre",{pre:!0,attrs:{class:"language-bash"}},[n("code",[e._v("$ "),n("span",{pre:!0,attrs:{class:"token function"}},[e._v("source")]),e._v(" mechwolf-env/bin/activate\n")])])]),n("p",[e._v("You can leave the virtualenv at any time with the command:")]),e._v(" "),n("div",{staticClass:"language-bash extra-class"},[n("pre",{pre:!0,attrs:{class:"language-bash"}},[n("code",[n("span",{pre:!0,attrs:{class:"token punctuation"}},[e._v("(")]),e._v("mechwolf-env"),n("span",{pre:!0,attrs:{class:"token punctuation"}},[e._v(")")]),e._v(" $ deactivate\n")])])])])},[],!1,null,null,null);t.default=r.exports}}]);