# Frogwatch

This branch of the Frogwatch program is for running as a CGI program within a web server with audio and image files served from the same machine.

The "frogs" variable is a list of lists. Each entry in "frogs" contains a base filename for both the image and audio files associated with the frog and the common name of the frog species. To use it, you must prepare your audio clips and images, saving them into a directory where the webserver will be able to serve them directly. In my case, I called the directory "Frogwatch" but you can change that by editing the imgurl and wavurl functions.

For instance, the American Bullfrog would be set up such that a relative link to "/Frogwatch/AmericanBullfrog.jpg" would retrieve the image, and "/Frogwatch/AmericanBullfrog.wav" would retrieve the audio recording.
