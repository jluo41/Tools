---
created: 2026-11-17T01:48
updated: 2026-11-18T18:32
---

### Meeting Ashley
- What is the main strength
- Background
- Data
	- Data Insights
### Element  / Call it Element or Call it like Brick?

UI Element
and Brick Element


- Element组成最终的delivery。
	- 所以做好一个delivery就是要把element做好
	- 比如一个section，element就包括句子。
- Element有自己的时间线 （所以要有之前的版本变化），有质量的高低 （所以要有rubric rating）
	- 当然也有decision points，比如如何改，为什么这样改，不那样改。
	- 有人的feedback。
		- 比如觉得这几个词不行， 这一段的乖乖的，或者这个人做了这样的editing之类的。都算是feedback。
	- 所以我们用各种mark
- Element： AI 要能做loop evaluation，
	- 直到自己觉得没问题了，高分通过，或者
	- 直到自己不行了，给出comments，等待human的feedback，以及理由
	- 所以AI可以给evaluation
	- 所以AI可以给action，给这种变化
	- 所以AI可以给comments
- Element： 要有mark，不同mark代表一类事物
	- 没有解决的mark要给人注意力，去解决他们

一种类比。比如冰砖组成一坨雕塑。旧时光里，是一个砖一个砖雕刻
现在有AI了，你是一泼水，就能去粗取精，给你一个雕塑。
但是AI出来的雕塑不是我们想要的。
所以我们想让AI泼水之后，自动tag一些重要的砖，这个有这个问题，那个有那个问题。然后我们可以给feedback。

这里我们想要几点。
第一： 为什么要有冰砖？为啥不是一大坨冰。
- 因为我们想要结构。
- 不是泼一次水，一个无定形的形状，水流走了，什么都没留下
第二：为什么要给冰砖贴标签。
* 因为我们要处理那个冰砖
* 不仅如此，我们还要储存冰砖的历史版本，我们是怎么一直更新冰砖的
第三：冰砖的标签，会不会太频繁，人疲于奔命
* 会的，所以我们要泼特别的水， 这个水可以自动处理很多tedious的标签，只把最critical的，需要思辨的砖的标签留下。这些也许是跟人交互最多的。
第四：同一类型的冰砖，可以生成这一类冰砖的多个实体吗？
* 类和instance之间的关系。

定义element，就是定义了雕塑。

如何泼出来一个最长的河，大浪淘沙，每次只留下了最重要的东西去思考。


### Paper Theme 

/lab PaperBlockPath
/lab new window PaperBlockPath


/hai-paper-draft workflow t02_xxxx_draft_task. 
大浪淘沙型。

* 这里的问题就是，每个下面的element是什么，要定义好这个elemet的问题
* 比如 一类就是
* > PaperBlock > jNN_Paper_Version > tNN_Task_Draft > VIEW_Draft > SEC_DraftLab > ELM_sentence, or ELM_paragraph, etc. 


应该也有几个其他的模式

/hai-paper-ideation workflow 

/hai-paper-story workflow 


### Paper Theme --> Separate the Idea as a New Block
Idea, should be a separate block. 
Story, should have a view-section for the novelty check. 



### Idea

CMS and Physician Workflow and Fatigue and Healthoutcome

REACH and Clinical Note and Physician Fatigue



### Theme Design
For the theme design, we should have the follow three views
- Folder Structure
	- How things are storages in the File System
- Element Structure
	- How UI is presenting the Folder Structure in the Website
- Session Structure
	- The View-Section that should record that the important session history, 
	- Like the session should keep recording the chat progress to the history.  and how each session episode is related to the each Fold & Element. 

### Samsung - EHR Streaming
How to make the EHR Streaming and respond to Jenna's question? 

Jenna
1. 📩 她的原话

问题 1  你们最终要哪些数据？请给出具体字段的完整清单。
        她手上那张表（36 个字段）是最新的吗？
        还要不要 CGM 设备数据或其他字段？

问题 2  为什么要比每天一次更新得更快？
        是哪个流程或用途需要这么快？
    