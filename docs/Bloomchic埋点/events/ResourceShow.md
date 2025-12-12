# ResourceShow

## 基本信息

- **事件显示名**: 资源位展示<br/>（含全站资源位）
- **事件英文名**: `ResourceShow`
- **所属模块**: 1.【首页】埋点
- **应埋点平台**: Android,Web,IOS

## 事件属性

| 属性英文名 | 属性显示名 | 数据类型 | 属性值示例或说明 | 应埋点平台 | 触发时机 | 备注 | 日期 |
| --- | --- | --- | --- | --- | --- | --- | --- |
| `page_code` | 页面位置 | STRING | 首页、商品列表、商品详情页、其他 | JavaScript | 资源位完整曝光时上报，滚动的资源位在每次切换素材时会上报一次事件<br/>(可以完全展示的资源位在完整展示时才上报，不能完整展示的则是露出标题时就上报)<br/>(分类区无法区分具体是哪个类别；skip_page_url在分类区时是上报第一个小区的跳转url) |  |  |
| `module_name` | 模块名称 | STRING | 上报以下区域代码层面的定位标识<br/>(目前仅包括首页的顶部轮播Banner、分类区、新品区、热销区、WeddingGuest、WeekendDating、VacayVibes、JustDropped、BestSellers、品牌介绍区、评论区、ins区),瀑布流运营位,商品集合页 | JavaScript |  |  |  |
| `web_resource_id` | 资源位id | STRING |  | JavaScript |  |  |  |
| `web_module_number` | 模块内资源位序号 | NUMBER | 当前资源位在模块内的位置序号 (比如分类区序号有1-8，顶部Banner不同位置上报1.1、1.2、1.3等等) | JavaScript |  |  |  |
| `collection_id` | 列表ID | STRING | LP页才上报 11.7新增 |  |  |  |  |
| `collection_name` | 列表名称 | STRING | LP页才上报 11.7新增 |  |  |  |  |
| `section_name` | 上报区分模块用的 | STRING |  |  |  |  |  |
| `module_type` | 模块类型 "module","item" | STRING | APP 3.1新增 |  |  |  |  |
| `media_url` | 资源图片链接 | STRING | APP 3.1新增 |  |  |  |  |
| `ad_pos_percent` | 资源位大小站屏幕的面积，view面积/屏幕面积 | NUMBER | APP 3.1新增 |  |  |  |  |
| `skip_page_url` | 跳转页面url | STRING |  | JavaScript |  |  |  |
| `title` | 显示的标题 | STRING | APP 3.9新增 |  |  |  |  |
| `type` | 外层的模块类型， | STRING | APP 3.9新增<br/>banner,image_list,products,title,info_swiper,blank,countdown,filter_tab,title_v2,bottom_title,products_v2,info_swiper_v2,behind,topbar,flow_ad,image,swiper_banner,email_subscription,products_horizontal_sliding |  |  |  |  |
| `ab_group` | AB实验组 |  |  |  |  |  |  |
| `display_type` | 显示类型 | STRING | atmosphere_floor氛围楼层,marketing_card 卡片 |  |  |  |  |
| `model_index` | 模块内序号 | NUMBER | APP 3.31新增 |  |  |  |  |
| `name` | 配置的名称 | STRING | APP 3.9新增 |  |  |  |  |
