# VideoPlayStop

## 基本信息

- **事件显示名**: 视频播放停止<br/>（离开，或者播放结束时上报）
- **事件英文名**: `VideoPlayStop`
- **所属模块**: 3.【商详页】的埋点
- **应埋点平台**: Android,Web,IOS

## 事件属性

| 属性英文名 | 属性显示名 | 数据类型 | 属性值示例或说明 | 应埋点平台 | 触发时机 | 备注 | 日期 |
| --- | --- | --- | --- | --- | --- | --- | --- |
| `current_page` | 页面 | STRING |  |  |  |  |  |
| `current_module` | 模块名 | STRING |  |  |  |  |  |
| `product_id` | 商品ID，商品视频才有 | STRING |  |  |  |  |  |
| `video_url` | 视频URL | STRING |  |  |  |  |  |
| `product_sku` | 商品SKU，可选，评论视频才有 | STRING |  |  |  |  |  |
| `product_spu` | 商品名，可选 | STRING |  |  |  |  |  |
| `product_name` | 商品名，可选 | STRING |  |  |  |  |  |
| `freeze_times` | 卡顿次数 | INT |  |  |  |  |  |
| `video_buffer_time` | 视频缓冲时间，视频实际开始播放时间 - 视频开始缓冲的时间 s 保留小数 | NUMBER |  |  |  |  |  |
| `play_video_time` | 观看时长，播放停止-视频实际开始播放时间，排除暂停和缓冲时间 s 保留小数 | NUMBER |  |  |  |  |  |
| `name` | 开屏广告活动名称 | STRING |  |  |  |  |  |
| `video_time` | 视频时长 s 保留小数 | NUMBER |  |  |  |  |  |
| `failed_reason` | 播放失败原因 | STRING |  |  |  |  |  |
