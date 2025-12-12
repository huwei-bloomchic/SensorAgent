# RecordWebPerformance

## 基本信息

- **事件显示名**: 记录web性能
- **事件英文名**: `RecordWebPerformance`
- **所属模块**: 0.全局埋点
- **应埋点平台**: Web

## 事件属性

| 属性英文名 | 属性显示名 | 数据类型 | 属性值示例或说明 | 应埋点平台 | 触发时机 | 备注 | 日期 |
| --- | --- | --- | --- | --- | --- | --- | --- |
| `pcPost_loaded` | 首页PC视频封面加载时间 | NUMBER |  |  |  |  |  |
| `firstImage_loaded` | 首页轮播图第一张加载时间 |  |  |  |  |  |  |
| `mobilePost_loaded` | 首页M视频封面加载时间 |  |  |  |  |  |  |
| `html_loaded` | 页面HTML文档完全加载时间 |  |  |  |  |  |  |
| `bootstrap` | LP页面vue客户端渲染组件挂载时间 |  |  |  |  |  |  |
| `productImage_loaded` | LP页面首个商品Item图片出现时间（近似LCP） |  |  |  |  |  |  |
| `ShopifyListData_load` | 调用shopify接口获取首页列表数据时间 |  |  |  |  |  |  |
| `ByteDanceListData_load` | 调用火山接口&查询shopify接口获取首页列表数据时间，首页列表数据加载完成时间 |  |  |  |  |  |  |
