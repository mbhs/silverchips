# Django News Layout

This file should provide a reasonable guide to the structure of the Django News
server.

## Django Applications

The primary Django applications in use are `news`, `core`, and `home`. The 
mentality behind this decision is that calling the Django build `djangonews` is
too lengthy and redundant. We can get around this by simply shortening it to 
`news` and compiling the apps that would, in theory, serve the web addresses
`/news`, `/opinions`, etc into a single app called `home`. Finally, `core` will
contain all models employed by the news website. Take note that the `docs` 
folder is not a Django application, and is instead a private directory 
containing the project documentation.

## Models

Currently, media models are separated into Audio, Video, and Images. This is to
keep them separate in the file system.
