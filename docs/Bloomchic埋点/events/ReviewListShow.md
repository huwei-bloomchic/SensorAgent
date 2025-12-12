# ReviewListShow

## 基本信息

- **事件显示名**: 评价列表展示
- **事件英文名**: `ReviewListShow`
- **所属模块**: 3.【商详页】的埋点
- **应埋点平台**: Android,Web,IOS

## 事件属性

| 属性英文名 | 属性显示名 | 数据类型 | 属性值示例或说明 | 应埋点平台 | 触发时机 | 备注 | 日期 |
| --- | --- | --- | --- | --- | --- | --- | --- |
| `review_from_module` | 评论列表来源入口 | STRING | 商品价格右侧评论、Fit 商详评论展示View All | JavaScript | 评价列表页展示时上报 |  |  |
| `product_spu` | 商品SPU | STRING | 当前商品SPU编号 | JavaScript |  |  |  |
| `product_name` | 商品名称 | STRING |  | JavaScript |  |  |  |
| `review_number` | 评价数量 | INT | 1) 通过审核的评价总数(人工审核、自动审核)：0、1、2、3...<br/>2) 当没有评价时，此时数量取0 | JavaScript |  |  |  |
| `average_overall_rating` | 综合评分均值 | NUMBER | 1) 取综合评分均值，小数点后一位：1、1.1、1.2...2.1、2.2...4.9、5<br/>2) 当评价数量为0时，此时的综合评分为0 | JavaScript |  |  |  |
