#Frameworks
Frameworks libraries (or a set of libraries, which may import more libraries if you wish) that have a pre-defined structure for writing an application. The most popular type of web application Framework is an **MVC**. These basically just help you organize your code and give you patterns and conventions to keep things from getting out of hand.

##MVC
**Model, View, Controller** style frameworks break code into pieces that relate to modelling data (**model**), pieces related to presenting or viewing that data (**view**) and code that is responsible for the logic related to handling requests and responses (**controllers**). Controllers are typically the part of the application that will connect to a db or other service and pass that data to the view code, which will generate the html for the web page to be sent back to the client. There is much discussion about variants of the MVC architecture - you may see MV\* or other similar types referenced in unnecessarily heated debates about the acronyms, but they all do basically the same thing: connect data to how you present it based on what the client asks for. 

##The Other Pieces - Routers and Templates
The **MVC** acronym overlooks the other two most important pieces of any framework - **templates** and the **router**. Templates are exactly that - some representation of how you present your data without any specific data filled in (so they can be resused no matter what the specific data may be). The router is what connects requests to controllers and ultimately views. When we look at Flask, the router is mostly abstracted away for us, but it is essentially the backbone of the application. Although to many MVCs views and templates are one in the same.

#Flask
Flask is a micro-framework for python. It is fairly simple to setup, and can help build applications very quickly. It is a little light to do anything very large, but it is good for many production applications and shouldn't be too much too soon. Please read and lookover the tutorial at http://flask.pocoo.org/docs/0.10/. Flask is not a true MVC, but could be treated like one. That is why it is a micro-framework.
