# 如何优雅的使用GitHub

-------

### GitHub是著名的分布式代码管理网站，程序猿必备，下面我带大家一步一步使用它；一步两步，摩擦...

## 1、注册GitHub
 - 登录[GitHub](github.com)
 - 点击`Singn up for GitHub`进行注册
 - 注册就不细说了，推荐使用Gmail邮箱。Why?逼格高！（其实是因为国内邮箱广告太多了，你看着会很乱，建议自己注册一个Gmail） 

## 2、创建项目
 - 点击右上角的`+`，单击`new repository`
 - 在repository name处填入你的项目名称，例如：Python_HomeWork
 - `Decription`是你这个项目的描述（简介）
 - 选择public（公开）
 - 点击最下方按钮`Create repository`创建项目
 
 #### 好了，这样你就有一个新的git线上仓库了，可以开始配置你的本地git程序了

-----------------

 - 使用source tree管理git
 - 使用原生git命令行管理git

# 使用source tree来管理


## 1、下载[SourceTree](https://www.sourcetreeapp.com/)代码管理工具(需要翻墙)
 - 刚给你们下好的链接：http://pan.baidu.com/s/1i5EaWPf 密码：ljwk
 - 安装过程一路下一步，需要登录的时候可以使用刚才注册的Gmail作为登录账户，进入官方网站进行授权。
 
## 2、创建本地仓库克隆
 - 点击tools=>options,Language处可以选择中文，建议使用英文（编程嘛，还是英文碰到的多，多使用英文软件有助于你以后水平的提高）
 - 点击`File`=》`Clone/NEW`
 - 在`Source Path/URL`处填入你GitHub项目的地址
  - 登录你的GitHub，点击项目进入项目主页，在项目右边点击`Clone or download`，点地址后面的按钮直接将地址复制到剪贴板
 - 在`Destination Path`栏点击Browse，选择一个本地的文件夹，你的远程代码将会存储在这里
 - `Name`处填入一个名字，这是你本地项目的标识
 - 点击最下方`Clone`
 - 好的，完成这些，你的GitHub仓库就创建完毕了

## 3、提交、推送
 - 当你对代码进行修改（创建文件、修改、删除等）时，你打开Source Tree，点击左边栏`working copy`会清晰的看到你更改了哪些内容
 - `Unstaged files`栏点击每个文件，可以看到你对文件的那部分进行了修改
 - 点击`Stage All`会将`Unstaged files`栏内所有文件进行暂存（相当于git的git add命令）
 - 在下方空白处填写提交信息，点击commit即可将文件暂存
  - 填写commit message时请使用标准的commit语法
  - 例如：`<feat>add FTP method`
  - <类型>描述（描述请使用英文，刚开始可能很难，慢慢就习惯了，很简单的，坚持！）
  - `<feat>`添加新特性
  - `<docs>`对描述文档的修改
  - `<fix>`对bug的修复
  - `<style>`格式修改，不影响代码
  - `<refactor>`对代码重构
  - `<test>`增加测试代码
 - 完成上面的操作，你的代码已经被暂存了，但是还没有上传到github，点击`push`，确定，把代码推送到github，完成！

## 4、有关分支、代码时光机等内容这里不做说明，各位可以一起讨论

----------------

# 使用git原生命令模式管理代码

 - 我已经写好了教程，直接点了看吧
 - [git教程](http://www.cnblogs.com/limich/p/7479143.html)
 - 这个例子是用的国内码云OSchina，你替换成自己的github地址即可
