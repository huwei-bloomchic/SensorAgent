# ProductShow

## 基本信息

- **事件显示名**: 商品在列表中的展示
- **事件英文名**: `ProductShow`
- **所属模块**: 2.【商品】相关埋点
- **应埋点平台**: Android,Web,IOS

## 事件属性

| 属性英文名 | 属性显示名 | 数据类型 | 属性值示例或说明 | 应埋点平台 | 触发时机 | 备注 | 日期 |
| --- | --- | --- | --- | --- | --- | --- | --- |
| `page_code` | 页面位置 | STRING | 必填*<br/>首页、商品集合页、商详页、搜索、订单列表、个人页、购物车、收藏列表、我的评论<br/>详细请参考页面以及来源定义 | JavaScript | ProductShow/ProductClick的埋点 中特别要注意 page_code,module_name 字段的上报，特别是请求火山那边推荐数据时的SPM要跟上报的page_code,module_name保持一致， SPM的规则是 BloomChic$##${page_code}$##${module_name} | section_name |  |
| `module_name` | 模块名称 | STRING | 必填*<br/>Daily Drops、Best sellers、You May Also Like、搜索结果页,商品集合页，(个人页)VIP，(搜索，搜索结果页)推荐，（购物车）凑单推荐<br/>详细请参考页面以及来源定义 | JavaScript |  | 这几个地方的ymsl都统一归到ymsl模块，不要再加页面<br/><br/>-会员:历史老版本的会员页会展示VIP的推荐商品，现在没有了<br/>-商详搭配Outfit浮层：历史版本有，现在没有了<br/>-搜索联想页：历史PC端在联系页有商品推荐，现在没有了 |  |
| `web_module_number` | 模块内资源位的序号 | NUMBER | 必填*<br/>模块内商品所在的位置<br/>（当来源为搜索结果页时，要上报商品在搜索结果页的第几位）<br/>从0开始 | JavaScript |  |  |  |
| `product_spu` | 商品SPU | STRING | 必填*<br/>当前商品SPU编号 | JavaScript |  |  |  |
| `product_name` | 商品名称 | STRING | 必填* | JavaScript |  |  |  |
| `product_handle` | 商品handle | STRING | 必填*<br/>APP 3.8新增 |  |  |  |  |
| `product_url` | 商品URL | STRING | 当前商品链接<br/>是否有存在的必要 废弃？ | JavaScript |  |  |  |
| `is_new` | 可用状态 | BOOL |  | JavaScript |  |  |  |
| `web_original_price` | 原价 | NUMBER |  | JavaScript |  |  |  |
| `web_current_price` | 价格 | NUMBER |  | JavaScript |  |  |  |
| `product_id` | Shopify Product ID | STRING | 必填*<br/>上报 7781546885290 来源gid://shopify/Product/7781546885290 |  |  |  |  |
| `web_discount_price` | 折扣 | NUMBER | 必填* | JavaScript |  |  |  |
| `collection_id` | 集合商品数据需要上报所在集合的ID | STRING | 在获取集合页的数据时必填 |  |  | 10.6(Android2.11/ios 2.9)新增 |  |
| `collection_handle` | 集合商品数据需要上报所在集合的handle | STRING | 在获取集合页的数据时必填<br/>APP 3.8新增 |  |  |  |  |
| `search_content` | 搜索结果的数据需要上报搜索关键词 | STRING | 搜索结果 |  |  | 10.6(Android2.11/ios 2.9)新增 |  |
| `parent_product_id` | 详情页相关数据上报所在详情页的Product_id | STRING | 10.6(Android2.11/ios 2.9)新增 |  |  | 10.6(Android2.11/ios 2.9)新增 |  |
| `mark_type` | 左上角角标类型：<br/>如果没有就空着，<br/>如果有记录：new、hot、sale<br/>25年11月20 日3.34新增 | STRING |  |  |  |  |  |
| `data_type` | 是否有销售、加购/收藏提醒；<br/>如果没有就空着，<br/>如果有就记录类型：sold、wishlist、cart<br/>25年11月20 日3.34新增 | STRING |  |  |  |  |  |
| `scm` | ABTest流量来源，未命中实验"", 命中推荐实验 上报对应实验值，"Shopify" or "ByteDance"<br/>对于LP，有另外的开关配置，如果在实验中的LP则上报实验值，不在实验的LP上报“{实验值}Other”<br/>对于搜索页，SCM上报为“Search{实验值}” | STRING | C端_3.12新增实验值：<br/>"Shopify" 、 "ByteDance"、<br/>搜索实验的神策的对应实验值："BackendA","BackendB","BackendC"…… |  |  |  |  |
| `product_events_id` | 商品活动ID | NUMBER | app3.12新增字段,有展示活动才上报，<br/>无活动默认传0 |  |  |  |  |
| `data_channel` | 真实数据来源："Shopify" 、 "ByteDance" or "Bytem" | STRING | 必填*<br/>默认 Shopify |  |  |  |  |
| `transdata` | 火山推荐的透传数据 | STRING | 火山的请求必填 |  |  |  |  |
| `media_url` | 当前（首图/视频）曝光的资源URL，包括图片or视频链接 | STRING | 必填*<br/>24.5.14 APP3.5新增 |  |  |  |  |
| `clearance_type` | 清仓商品类型 | STRING | 新增字段，商品清仓类型<br/>- 非清仓：no_clearance<br/>- 全部清仓:clearance<br/>- 部分清仓:partial_clearance |  |  |  |  |
| `is_quickship_icon` | 是否有quickship标记 | BOOLEAN |  |  |  |  |  |
| `filter` | LP页有筛选条件时上报，筛选条件JSON | STRING | 24.5.14 APP3.5新增 |  |  |  |  |
