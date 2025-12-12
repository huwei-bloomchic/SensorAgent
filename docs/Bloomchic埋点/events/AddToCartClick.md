# AddToCartClick

## 基本信息

- **事件显示名**: 成功加入购物车
- **事件英文名**: `AddToCartClick`
- **所属模块**: 3.【商详页】的埋点
- **应埋点平台**: Android,Web,IOS

## 事件属性

| 属性英文名 | 属性显示名 | 数据类型 | 属性值示例或说明 | 应埋点平台 | 触发时机 | 备注 | 日期 |
| --- | --- | --- | --- | --- | --- | --- | --- |
| `product_from_page` | 商品来源页面 | STRING | 首页-Just dropped、首页-Best sellers、商品列表-ID、You may also like、 Customer Also Bought、搜索结果页、商详搭配Outfit浮层 | JavaScript | 点击加入购物车时上报 | 2021.11.4 18:00后生效Customer also bought<br/>2021.11.8 12:00后生效搜索结果页 |  |
| `from_page` | 来源页面 | STRING | APP 3.11版本修改，来自来源页面的模块<br/>神策上报页面以及页面来源规范梳理 |  |  |  |  |
| `from_module` | 来源模块 | STRING | APP 3.11版本修改，来自来源页面的模块<br/>神策上报页面以及页面来源规范梳理 | JavaScript |  |  |  |
| `page_code` | 当前页面 | STRING | APP 3.11版本修改<br/>按照既定规则 上报page_code & module_name<br/>page_code:<br/>商详页的page_code：商详页<br/>微商详的page_code：打开微商详的当前页面 | JavaScript |  |  |  |
| `module_name` | 当前模块名称 | STRING | APP 3.11版本修改<br/>按照既定规则 上报page_code & module_name<br/>module_name: 弹窗被认为主页面的模块，因此微商详弹窗应该上报 “微商详”<br/>商详页的module_name：商详页<br/>微商详的module_name：微商详 | JavaScript |  |  |  |
| `product_spu` | 商品SPU | STRING | 当前商品SPU编号 | JavaScript |  |  |  |
| `product_sku` | 商品SKU | STRING | 加入购物车的商品SKU编码 | JavaScript |  |  |  |
| `product_name` | 商品名称 | STRING | 商品名称 | JavaScript |  |  |  |
| `product_id` | Shopify Product ID | STRING | 上报 7781546885290 来源gid://shopify/Product/7781546885290 |  |  |  |  |
| `web_original_price` | 原价 | NUMBER |  | JavaScript |  |  |  |
| `web_current_price` | 价格 | NUMBER |  | JavaScript |  |  |  |
| `web_discount_price` | 折扣 | NUMBER |  | JavaScript |  |  |  |
| `product_events_id` | 商品活动ID | NUMBER | app3.12新增字段,有展示活动才上报，<br/>无活动默认传0 |  |  |  |  |
| `product_size` | 尺码 | STRING | 加入购物车的商品尺码 | JavaScript |  |  |  |
| `product_colour` | 颜色 | STRING | 加入购物车的商品颜色 |  |  |  |  |
| `clearance_type` | 清仓商品类型 | STRING | 新增字段，类型<br/>- 非清仓：no_clearance<br/>- 清仓:clearance |  |  |  |  |
| `return_type` | 退货类型 | STRING | 退货政策：<br/>-可退：return<br/>-不可退：no_return |  |  |  |  |
| `is_quickship` | 是否整单quickship仓发货 | BOOLEAN |  |  |  |  |  |
| `recommend_size` | 虚拟字段：combine_recommend_size | STRING | 推荐的尺码<br/>推荐成功 "10/M" ...<br/>其它没有推荐："" or NULL |  |  |  |  |
| `mark_type` | 左上角角标类型：<br/>如果没有就空着，<br/>如果有记录：new、hot、sale<br/>25年11月20 日3.34新增 | STRING |  |  |  |  |  |
| `data_type` | 是否有销售、加购/收藏提醒；<br/>如果没有就空着，<br/>如果有就记录类型：sold、wishlist、cart<br/>25年11月20 日3.34新增 | STRING |  |  |  |  |  |
| `is_preorder` | 是否预售，即是否有预售图表标记 | BOOL |  |  |  |  |  |
| `failed_reason` |  |  | 推荐失败的原因<br/>推荐成功："" or NULL<br/>品类不支持 "NotAvailable"<br/>没有登录 "Guest"<br/>没有填写胸围 "No Bust"<br/>没有合适尺码 "NoFitSize"<br/>其它没有推荐："Failed" | JavaScript |  |  |  |
| `is_preorder` | 是否预售，即是否有预售图表标记 | BOOL |  |  |  |  |  |
