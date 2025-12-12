# ProductPageShow

## 基本信息

- **事件显示名**: 商品详情页展示/ 微商详展示 （APP 3.9 新增）
- **事件英文名**: `ProductPageShow`
- **所属模块**: 3.【商详页】的埋点
- **应埋点平台**: Android,Web,IOS

## 事件属性

| 属性英文名 | 属性显示名 | 数据类型 | 属性值示例或说明 | 应埋点平台 | 触发时机 | 备注 | 日期 |
| --- | --- | --- | --- | --- | --- | --- | --- |
| `product_from_page` | 商品来源页面 | STRING | 首页-Just dropped、首页-Best sellers、商品列表-ID、You may also like、 Customer Also Bought、搜索结果页、个人页、商详搭配Outfit浮层 | JavaScript |  |  |  |
| `from_page` | 来源页面 | STRING | APP 3.11版本修改，来自来源页面的模块<br/>神策上报页面以及页面来源规范梳理 |  |  |  |  |
| `from_module` | 来源模块 | STRING | APP 3.11版本修改，来自来源页面的模块<br/>神策上报页面以及页面来源规范梳理 | JavaScript |  |  |  |
| `page_code` | 当前页面 | STRING | APP 3.11版本修改<br/>按照既定规则 上报page_code & module_name<br/>page_code:<br/>商详页的page_code：商详页<br/>微商详的page_code：打开微商详的当前页面 | JavaScript |  |  |  |
| `module_name` | 当前模块名称 | STRING | APP 3.11版本修改<br/>按照既定规则 上报page_code & module_name<br/>module_name: 弹窗被认为主页面的模块，因此微商详弹窗应该上报 “微商详”<br/>商详页的module_name：商详页<br/>微商详的module_name：微商详 | JavaScript |  |  |  |
| `page_type` | 页面类型，"商详页"，"微商详"<br/>区分是否是微商详 | STRING | APP 3.9版本新增<br/>商详页，微商详 |  |  |  |  |
| `product_spu` | 商品SPU | STRING | 当前商品SPU编号 | JavaScript |  |  |  |
| `product_name` | 商品名称 | STRING |  | JavaScript |  |  |  |
| `is_available` | 可用状态 | BOOL | 仅当该商品的所有规格都无货时会触发会上报false | JavaScript |  |  |  |
| `web_original_price` | 原价 | NUMBER |  | JavaScript |  |  |  |
| `web_current_price` | 价格 | NUMBER |  | JavaScript |  |  |  |
| `product_id` | Shopify Product ID | STRING | 上报 7781546885290 来源gid://shopify/Product/7781546885290 |  |  |  |  |
| `web_discount_price` | 折扣 | NUMBER |  |  |  |  |  |
| `product_skc_tag_{tag_style}` | SKC标签的颜色列表 | STRING | APP 3.8版本新增<br/>tag_style: new，配置的图片tag_style，用；分割:<br/>product_skc_tag_new:red;black |  |  |  |  |
| `quickship_skus` | quickship仓发货的SKU编码 | STRING |  |  |  |  |  |
| `preorder_skus` | 预售的SKU列表 | STRING | APP 3.8版本新增 使用 ";" 拼接 | JavaScript |  |  |  |
| `is_productcoutdown` | 是否有活动倒计时 | STRING | app3.12删除 | JavaScript |  |  |  |
| `product_events_id` | 商品活动ID | NUMBER | app3.12新增字段,有展示活动才上报，<br/>无活动默认传0 |  |  |  |  |
| `is_deliveryreminder` | 是否有发货提醒 | STRING |  | JavaScript |  |  |  |
| `clearance_type` | 清仓商品类型 | STRING | 新增字段，商品清仓类型<br/>- 非清仓：no_clearance<br/>- 全部清仓:clearance<br/>- 部分清仓:partial_clearance |  |  |  |  |
| `mark_type` | 左上角角标类型：<br/>如果没有就空着，<br/>如果有记录：new、hot、sale<br/>25年11月20 日3.34新增 | STRING |  |  |  |  |  |
| `data_type` | 是否有销售、加购/收藏提醒；<br/>如果没有就空着，<br/>如果有就记录类型：sold、wishlist、cart<br/>25年11月20 日3.34新增 | STRING |  |  |  |  |  |
| `return_type` | 退货类型 | STRING | 退货政策：<br/>-可退：return<br/>-部分可退：partial_return<br/>-不可退：no_return |  |  |  |  |
