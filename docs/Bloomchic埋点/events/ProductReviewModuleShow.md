# ProductReviewModuleShow
（之前的ProductReviewShow有几条优质评论就上报几次）

## 基本信息

- **事件显示名**: 商详评论模块展示（这个评论模块的展示上报）
- **事件英文名**: `ProductReviewModuleShow
（之前的ProductReviewShow有几条优质评论就上报几次）`
- **所属模块**: 3.【商详页】的埋点
- **应埋点平台**: Android,Web,IOS

## 事件属性

| 属性英文名 | 属性显示名 | 数据类型 | 属性值示例或说明 | 应埋点平台 | 触发时机 | 备注 | 日期 |
| --- | --- | --- | --- | --- | --- | --- | --- |
| `product_spu` | 商品SPU | STRING | 当前商品SPU编号 | JavaScript | 进入当前商详页之后，在此商详页只上报一次<br/>商详滑动此模块时上报，包含评论总评分星级模块和商详展示的用户模块内容。 |  |  |
| `product_id` | 商品ID |  |  |  |  |  |  |
| `review_show_number` | 展示的评价个数 | INT | 0 无评论数<br/>1 只有一条优质评论<br/>2<br/>3 |  |  |  |  |
| `review_number` | 评价总数量 | INT | 该商品的评论总数， |  |  |  |  |
| `average_overall_rating` | 综合评分均值 | NUMBER | 1) 取综合评分均值，小数点后一位：1、1.1、1.2...2.1、2.2...4.9、5<br/>2) 当评价数量为0时，此时的综合评分为0 |  |  |  |  |
