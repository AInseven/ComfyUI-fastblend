# ComfyUI-fastblend
fastblend for comfyui, and other nodes that I write for video2video. rebatch image, my openpose

fastblend的节点：
1.smoothvideo（逐帧渲染）
2.interpolateKeyFrame（插帧，只选一部分帧渲染）

我自己做视频用的节点：
1.rebatchimage，为fastblend写的节点，同时渲染n张图(720p 24G显存batch_size可以调整到40)，提速约40%。
2.mpopenpose,因为dwopenpose在人物转身的时候不能识别人物后背，但是在人物姿势方便比openpose准确，而openpose可以很好的识别后背，这个就是结合了它两的优点

例子在我上传的.json里，还有别的节点其实没多大用，有的还用不成，就不介绍了。

安装：下载.zip解压到ComfyUI\custom_nodes就可以了


