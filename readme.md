需要安装Python3.11版本: [Download Python | Python.org](https://www.python.org/downloads/)
需要安装PIL库: `pip install pillow`



整合和修改饥荒mod制作时用到的动画和图片工具
- 使用这个工具时会将所有symbol名转换为小写(因为饥荒不区分大小写)

- 自动补充复用的图片, 图片名包含(druation'num'), num为使用第几张补充，用透明图补充缺少的图片, 图片名包含(missing)，在打包时自动忽略

- 修复解包和打包时使用正确的图层名(命名图层名时按 图层名_000的格式,如arm_upper_000, arm_upper_001)

- 修复解包一些文件时图片拉伸错误，打包时自动去除图片多余的透明部分

- 由于饥荒是按照固定帧率(一般为30)播放动画, 为了保证动画的一致性, 所以在导出scml时只保证关键帧生成正确，并且打包时提供的scml文件必须按照30帧(每33间隔一帧)

- 修复打包的动画无法选中的问题

  

使用: 将要转的文件用鼠标拖到convert.bat上
1. 传入文件json文件与bin文件互相转换, 传入zip则自动转换zip里的内容  
2. 传入dyn文件,转换成zip格式, 修改自: https://github.com/UNOWEN-OwO/dyn_decrypt  
3. tex与png互转  
   tex转png使用ktech: https://github.com/nsimplex/ktools  
   png转tex使用klei的TextureConverter: https://github.com/kleientertainment/ds_mod_tools  
4. 传入文件夹(按下面顺序查找文件夹)：  
    (1) 有tex文件和对应xml文件, 自动拆图  
    (2) 有png文件, 自动合并成一张图并生成xml(atlas名为文件夹名)  
           如果atals名中有inventoryimages, 自动将图片调整成64×64, 有cookbook, 自动调整为256×256,并且自动加入前缀cookbook_，可在keli/properties.py里自行添加  
    (3) 有dyn文件, 自动转换成压缩包  
    (4) 有scml文件, 自动打包(build名位scml文件名), 打包时输入图片的缩放(默认1)  
    (5) 文件夹里有zip文件, 自动合并zip文件并转换成scml(输出的build名位文件夹名) 修改自: https://github.com/nsimplex/ktools  
            修改klei/symbol_map.py里的SymbolMap可以自动修改转为scml时的symbol名(在转换时输入1)  
    (6) 文件夹里有拆包得到的json文件和图片, 自动打包(可修改build里的scale来修改打包时的缩放)  
