# ComfyUI-fastblend
fastblend for comfyui, and other nodes that I write for video2video. rebatch image, my openpose

fastblend node：  
1.smoothvideo（逐帧渲染/smooth video use each frames）  
2.interpolateKeyFrame（插帧、只选一部分帧渲染/smooth video only use a portion of the frames）

other nodes for making video:  
1.rebatchimage: especially for fastblend，Simultaneously render images (720p, 24G video memory, batch_size can be adjusted to 40), speed up about 40%.  
2.myopenpose,因为dw_openpose在人物转身的时候不能识别人物后背，但是在人物姿势方面比openpose准确，而openpose可以很好的识别后背，这个就是结合了它两的优点

examples are in example directory.And other nodes don't have much use,so I'm not going to introduce.

Install：download the .zip and unzip to ComfyUI\custom_nodes.

Fastblend main code is from https://github.com/Artiprocher/sd-webui-fastblend
I just made it work in ComfyUI.
