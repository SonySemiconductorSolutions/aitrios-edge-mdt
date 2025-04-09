## <div align="center">Post Processing</div>

🧮 **Note:** This topic is intended for advanced users. If this is your first use of Edge-MDT for converting a model to run on Edge AI Processor, it is advisable not to start from this model, but rather with a simpler model that does not include Post Processing.

This page explains the following topics:
*	What is post processing
*	What are the considerations for running post processing on the host CPU or on the Edge AI Processor
*	The mechanisms that Edge-MDT offers for running post processing blocks on the Edge AI Processor

### What is post processing ###
Post processing (PP) is a general term for layers or operators that occur ‘after’ the model. Typically, these are layers without any trainable parameters, layers that are take the output of the model and process it for the application.<br>
For example: models from the family of object detection use NMS.

<br>
<div align="center" markdown="1">
<p>
      <img src="https://github.com/SonySemiconductorSolutions/aitrios-edge-mdt/blob/Post-processing-doc/docs/images/post-processing/post%20processing%20blocks.png">
This diagram depicts a schematic split of the dataflow pipeline into the model, post processing and application.
</p>
</div>
<br>

The Edge AI processor offers a unique mechanism that allows to run post processing more efficiently in terms of latency and power consumption. By using this mechanism it is possible to improve the overall system performance.<br> <br>
In a typical implementation of an AI feature, the inference stage run on the Edge AI Processor accelerator, the Edge AI Processor then sends the outcome of the inference to the host CPU. The host CPU takes that as input, and uses it as part of the application itself.<br>
Post processing blocks are the last part of the inference, or the early part of the application. In many cases they can just run on the host CPU and not on the Edge AI Processor, but in some cases there are reasons to run them on the Edge AI Processor.

<br>
<div align="center" markdown="1">
<p>
      <img src="https://github.com/SonySemiconductorSolutions/aitrios-edge-mdt/blob/Post-processing-doc/docs/images/post-processing/post_processing_blocks_1.png">
In the upper part of the diagram post processing is run on the host, whereas in the lower part, it is run on the Edge AI Processor.
</p>
</div>
<br>

### Deciding where post processing should run ###
The Edge-MDT user needs to make an architecture decision which parts should run on the Edge AI Processor, and which parts should run on the host CPU.
When making such a decision the user should consider the following aspects:
*	The Edge AI Processor is a strong accelerator for running heavy workloads in a fast and efficient manner, but it does not always support running any PP operator
*	Consider the load of running the PP blocks on the host CPU, as PP can sometimes be a heavy computation, and the host CPU might be too weak to carry a heavy workload
*	Latency caused by running on the host CPU - a weak CPU may take significantly more time to run PP, and affect the overall latency and FPS
*	Running PP blocks on the host CPU can cause the sending of large amounts of data from the Edge AI Processor to the CPU. Depending on the interface between the Edge AI Processor and the CPU, and the efficiency of the host CPU software in handling large memory chunks, this may cause a latency hit
*	Power consumption
*	Ease of implementation

When taking into account the considerations, there could be various cases in which there’s an important benefit to running PP on the Edge AI Processor.<br>
Edge-MDT offers the following options for running PP workloads on the Edge AI Processor:
*	16bit quantization for selected layers – by setting PP operators to run in 16bit quantization bit-width, the overall accuracy is improved, with a relatively small impact on memory size
*	Custom Layers – Edge-MDT supports several common layers that can be converted to run on the Edge AI Processor.

### 16bit quantization for selected layers ###
Edge-MDT supports large span of layers and operators that can be converted to run on the Edge AI Processor. In case the post processing is fully comprised from such building blocks, then the user can just convert them to run on the Edge AI Processor. <br>
In the typical case it would mean that such layers will need to be configured to use 16bit quantization bit-width.<br>
The user can achieve it by either using the automatic mixed-precision mode of MCT, or manually set specific layers to use 16bit. For more info please refer to [MCT documentation](https://github.com/sony/model_optimization).

Note that the use of 16bit quantization for specific layers is considered an advanced feature, since the user might need to dive into the accuracy optimization of the model.

### Custom Layers ###
In case the operators that comprise the PP block cannot be converted to run on the Edge AI Processor, Edge-MDT provides a set of methods that can be used. <br>
For example the following layers are available in Pytorch: NMS, NMS with indices.<br>
Custom layer is an implementation of PP block in a way that can be converted to run on the Edge AI Processor.<br>
For example, suppose the PP phase includes Pytorch NMS layer, this layer cannot be converted to run on the Edge AI Processor. The user can replace the Pytorch NMS layer with the NMS layer from the custom layer library.<br>
Using a custom layer basically means replacing a layer from the model with another layer, and typically the user would need to adjust the code to fit the Custom Layer method. This is because there are various implementations of NMS, and they are not always taking the same input, and returning the same outputs.<br>

<br>
<div align="center" markdown="1">
<p>
      <img src="https://github.com/SonySemiconductorSolutions/aitrios-edge-mdt/blob/Post-processing-doc/docs/images/post-processing/post_processing_blocks_2.png"><br>
The diagram depicts a design where post processing is run on the Edge AI Processor by using a Custom Layer. The 'pre' part needs to be adjusted to run on the Edge AI Processor using operators that can be converted to run on it. The Custom Layer is the last part that runs on the Edge AI Processor, and the 'post' part runs already on the host CPU.
</p>
</div>
<br>

For more information on custom layers and how to use them please refer to the [custom layers documentation](https://github.com/sony/custom_layers/tree/main/tutorials/pytorch).

Note that the use of custom layers is considered an advanced feature, since the user will need to make changes to the code of the model, find how to peel off an existing layer and replace it with the custom layer.

### Summary ###
To summarize, there are several mechanisms in Edge-MDT that the user can utilize in order to implement post processing for a specific model.
