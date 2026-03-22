#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Iceberg Spark v3.4 模块源码设计文档生成脚本"""
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import mm, cm
from reportlab.lib.colors import HexColor, black, white
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_JUSTIFY
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
import os, platform

def register_fonts():
    system = platform.system()
    paths = {
        'Darwin': [('/System/Library/Fonts/STHeiti Medium.ttc','STHeiti'),('/System/Library/Fonts/PingFang.ttc','PingFang'),('/Library/Fonts/Arial Unicode.ttf','ArialUnicode')],
        'Linux': [('/usr/share/fonts/truetype/wqy/wqy-zenhei.ttc','WenQuanYi')],
        'Windows': [('C:/Windows/Fonts/msyh.ttc','MicrosoftYaHei')],
    }
    for p,n in paths.get(system,[]):
        if os.path.exists(p):
            try:
                pdfmetrics.registerFont(TTFont(n,p)); return n
            except: continue
    return 'Helvetica'

FN = register_fonts()
styles = getSampleStyleSheet()
C = {'p':HexColor('#1a237e'),'s':HexColor('#283593'),'a':HexColor('#e65100'),'bl':HexColor('#e8eaf6'),
     'bm':HexColor('#c5cae9'),'bd':HexColor('#3949ab'),'t':HexColor('#212121'),'tl':HexColor('#757575'),
     'bo':HexColor('#bdbdbd'),'g':HexColor('#2e7d32'),'o':HexColor('#ef6c00'),'r':HexColor('#c62828'),
     'b':HexColor('#1565c0'),'pu':HexColor('#6a1b9a'),'te':HexColor('#00695c')}

ts=ParagraphStyle('T',parent=styles['Title'],fontName=FN,fontSize=28,textColor=C['p'],spaceAfter=20,alignment=TA_CENTER,leading=36)
ss=ParagraphStyle('S',parent=styles['Normal'],fontName=FN,fontSize=14,textColor=C['tl'],spaceAfter=30,alignment=TA_CENTER,leading=20)
h1=ParagraphStyle('H1',parent=styles['Heading1'],fontName=FN,fontSize=20,textColor=C['p'],spaceBefore=24,spaceAfter=12,leading=28)
h2=ParagraphStyle('H2',parent=styles['Heading2'],fontName=FN,fontSize=16,textColor=C['s'],spaceBefore=16,spaceAfter=8,leading=22)
h3=ParagraphStyle('H3',parent=styles['Heading3'],fontName=FN,fontSize=13,textColor=C['a'],spaceBefore=12,spaceAfter=6,leading=18)
bs=ParagraphStyle('B',parent=styles['Normal'],fontName=FN,fontSize=10,textColor=C['t'],spaceBefore=4,spaceAfter=4,leading=16,alignment=TA_JUSTIFY)
cs=ParagraphStyle('C',parent=styles['Normal'],fontName=FN,fontSize=9,textColor=C['tl'],spaceBefore=4,spaceAfter=8,alignment=TA_CENTER,leading=13)

def mt(data,cw=None,hc=None):
    if cw is None: cw=[480]
    if hc is None: hc=C['bd']
    t=Table(data,colWidths=cw)
    t.setStyle(TableStyle([('BACKGROUND',(0,0),(-1,0),hc),('TEXTCOLOR',(0,0),(-1,0),white),
        ('FONTNAME',(0,0),(-1,-1),FN),('FONTSIZE',(0,0),(-1,0),10),('FONTSIZE',(0,1),(-1,-1),8.5),
        ('ALIGN',(0,0),(-1,-1),'CENTER'),('VALIGN',(0,0),(-1,-1),'MIDDLE'),
        ('GRID',(0,0),(-1,-1),0.5,C['bo']),('ROWBACKGROUNDS',(0,1),(-1,-1),[white,C['bl']]),
        ('TOPPADDING',(0,0),(-1,-1),5),('BOTTOMPADDING',(0,0),(-1,-1),5),
        ('LEFTPADDING',(0,0),(-1,-1),6),('RIGHTPADDING',(0,0),(-1,-1),6)]))
    return t

def mi(data,cw=None):
    if cw is None: cw=[80,400]
    t=Table(data,colWidths=cw)
    t.setStyle(TableStyle([('BACKGROUND',(0,0),(0,-1),C['bl']),('FONTNAME',(0,0),(-1,-1),FN),
        ('FONTSIZE',(0,0),(-1,-1),9),('ALIGN',(0,0),(0,-1),'RIGHT'),('ALIGN',(1,0),(1,-1),'LEFT'),
        ('VALIGN',(0,0),(-1,-1),'MIDDLE'),('GRID',(0,0),(-1,-1),0.5,C['bo']),
        ('TOPPADDING',(0,0),(-1,-1),5),('BOTTOMPADDING',(0,0),(-1,-1),5),
        ('LEFTPADDING',(0,0),(-1,-1),8),('RIGHTPADDING',(0,0),(-1,-1),8)]))
    return t

def build():
    op=os.path.join(os.path.dirname(os.path.abspath(__file__)),'Iceberg_Spark_v3.4_Design_Document.pdf')
    doc=SimpleDocTemplate(op,pagesize=A4,topMargin=2*cm,bottomMargin=2*cm,leftMargin=2*cm,rightMargin=2*cm)
    st=[]
    # 封面
    st.append(Spacer(1,80))
    st.append(Paragraph('Apache Iceberg',ts))
    st.append(Paragraph('Spark v3.4 集成模块源码设计文档',ParagraphStyle('s2',parent=ts,fontSize=22,spaceAfter=20)))
    st.append(Spacer(1,10))
    st.append(Paragraph('基于 Apache Iceberg v1.9.2 源码深度分析',ss))
    st.append(Spacer(1,30))
    st.append(mi([['项目','Apache Iceberg - Spark v3.4 Integration'],['版本','v1.9.2'],
        ['模块','spark/v3.4/spark + spark-extensions'],['规模','~594 文件 (503 Java + 91 Scala)'],
        ['Spark 版本','Apache Spark 3.4.x'],['文档类型','源码架构与设计分析']],[140,320]))
    st.append(PageBreak())

    # 目录
    st.append(Paragraph('目录',h1))
    for i,t in enumerate(['第一章 整体架构概览','第二章 核心流程图','第三章 核心时序图',
        '第四章 核心类设计说明','第五章 关键设计模式总结']):
        st.append(Paragraph(t,ParagraphStyle('toc',parent=bs,fontSize=12,textColor=C['p'])))
    st.append(PageBreak())

    # 第一章
    st.append(Paragraph('第一章  整体架构概览',h1))
    st.append(Paragraph('1.1 模块结构与分层架构',h2))
    st.append(Paragraph('Iceberg Spark v3.4 集成模块是 Apache Iceberg 与 Apache Spark 3.4.x 之间的桥梁层，负责将 Iceberg 的表格式能力（ACID 事务、Schema 演进、时间旅行、分区演进等）无缝暴露给 Spark SQL 引擎。该模块通过实现 Spark DataSource V2 API，使得用户可以通过标准 Spark SQL 语法操作 Iceberg 表。',bs))
    st.append(mt([['层次','模块/包','职责','关键类'],
        ['SQL 扩展层','spark-extensions','ANTLR 语法扩展、\n分析/优化规则注入','IcebergSparkSession\nExtensions'],
        ['Catalog 适配层','o.a.i.spark','Spark Catalog 到\nIceberg Catalog 桥接','SparkCatalog\nSparkSessionCatalog'],
        ['数据源层','o.a.i.spark.source','DSv2 实现：读/写/表','SparkTable, SparkScan\nSparkWrite, SparkBatch'],
        ['Filter/类型层','o.a.i.spark','Expression 转换','SparkV2Filters\nSparkSchemaUtil'],
        ['数据读写层','o.a.i.spark.data','Parquet/ORC/Avro\n格式读写','SparkParquetReaders\nSparkParquetWriters'],
        ['向量化读取层','o.a.i.spark.data\n.vectorized','列式批量读取','VectorizedSpark\nParquetReaders'],
        ['Actions 层','o.a.i.spark.actions','表维护操作','SparkActions\nRewriteDataFiles'],
        ['Procedures 层','o.a.i.spark.procedures','SQL CALL 命令','SparkProcedures\nBaseProcedure'],
        ['Functions 层','o.a.i.spark.functions','内置 UDF','BucketFunction\nTruncateFunction']
    ],[80,100,115,125]))
    st.append(Paragraph('图 1-1: Spark v3.4 模块分层架构',cs))

    st.append(Paragraph('1.2 与 Spark DataSource V2 API 的对接模型',h2))
    st.append(Paragraph('Iceberg 通过实现 Spark DSv2 核心接口来完成集成，以下是关键接口对接关系：',bs))
    st.append(mt([['Spark DSv2 接口','Iceberg 实现','功能'],
        ['TableCatalog\nSupportsNamespaces','SparkCatalog','表/命名空间 CRUD'],
        ['Table, SupportsRead\nSupportsWrite, SupportsDeleteV2','SparkTable','单表读写删除入口'],
        ['ScanBuilder\nSupportsPushDown*','SparkScanBuilder','扫描计划构建\n谓词/列/聚合/Limit下推'],
        ['Scan, SupportsReport\nStatistics','SparkScan\nSparkBatchQueryScan','执行扫描\n统计/批处理/流处理'],
        ['WriteBuilder\nSupportsDynamic/Overwrite','SparkWriteBuilder','写入计划构建'],
        ['Write, RequiresDistribution\nAndOrdering','SparkWrite','执行写入\n分发/排序/分区'],
        ['DeltaWrite','SparkPositionDeltaWrite','MoR 行级操作'],
        ['DataSourceRegister','IcebergSource','数据源注册入口']
    ],[130,110,190],C['p']))
    st.append(Paragraph('图 1-2: Spark DSv2 接口与 Iceberg 实现对接',cs))
    st.append(PageBreak())

    # 第二章
    st.append(Paragraph('第二章  核心流程图',h1))
    st.append(Paragraph('2.1 Spark SQL 查询 Iceberg 表全流程',h2))
    st.append(mt([['步骤','组件','操作描述'],
        ['1','Spark SQL Parser','解析 SQL，生成逻辑计划'],['2','SparkCatalog','loadTable(): 加载 Iceberg Table'],
        ['3','SparkTable','newScanBuilder(): 创建 SparkScanBuilder'],
        ['4','SparkScanBuilder','pushPredicates(): SparkV2Filters 转换谓词并下推'],
        ['5','SparkScanBuilder','pruneColumns(): 列裁剪(含元数据列)'],
        ['6','SparkScanBuilder','pushAggregation(): 聚合下推(COUNT/MIN/MAX)'],
        ['7','SparkScanBuilder','pushLimit(): 行数限制下推'],
        ['8','SparkScanBuilder','build() -> SparkBatchQueryScan'],
        ['9','SparkBatchQueryScan','taskGroups(): scan.planFiles() 生成 FileScanTask'],
        ['10','SparkBatch','planInputPartitions(): 分配任务给 Executor'],
        ['11','Executor','RowDataReader 读取数据 + DeleteFilter 过滤']
    ],[30,115,325],C['b']))
    st.append(Paragraph('图 2-1: 查询全流程',cs))

    st.append(Paragraph('2.2 Spark 写入 Iceberg 表全流程',h2))
    st.append(mt([['步骤','组件','操作描述'],
        ['1','SparkTable','newWriteBuilder(): 创建 SparkWriteBuilder'],
        ['2','SparkWriteBuilder','校验/合并 Schema, 确定写入模式'],
        ['3','SparkWriteBuilder','build() -> SparkWrite 匿名子类'],
        ['4','SparkWrite.toBatch()','返回 BatchAppend/DynamicOverwrite/OverwriteByFilter/COW/Rewrite'],
        ['5','WriterFactory','在 Executor 创建 PartitionedDataWriter/UnpartitionedDataWriter'],
        ['6','DataWriter','write(): 计算 PartitionKey, 写入文件(RollingDataWriter控制大小)'],
        ['7','DataWriter','commit() -> TaskCommit(DataFile[])'],
        ['8','Driver','收集 TaskCommit, 调用 Iceberg API: newAppend/newOverwrite'],
        ['9','commitOperation()','设置 appId/WAP/Branch, 执行 OCC commit()']
    ],[30,115,325],C['g']))
    st.append(Paragraph('图 2-2: 写入全流程',cs))

    st.append(Paragraph('2.3 SparkCatalog 加载表流程',h2))
    st.append(mt([['步骤','方法','操作描述'],
        ['1','loadTable(ident)','入口: 调用 load(ident)'],
        ['2','判断 PathIdentifier','路径标识: HadoopTables.load()'],
        ['3','icebergCatalog.loadTable()','通过 Iceberg Catalog 加载(支持 CachingCatalog)'],
        ['4','new SparkTable(table)','包装为 SparkTable'],
        ['5','表名后缀解析','失败回退: namespace 作为表名, name 作为后缀'],
        ['6a','at_timestamp_xxx','时间旅行: SnapshotUtil.snapshotIdAsOfTime()'],
        ['6b','snapshot_id_xxx','快照定位: 直接使用 snapshotId'],
        ['6c','branch_xxx','分支: copyWithBranch()'],
        ['6d','tag_xxx','标签: 获取 tag 对应 snapshotId'],
        ['6e','changelog','返回 SparkChangelogTable']
    ],[30,115,325],C['a']))
    st.append(Paragraph('图 2-3: SparkCatalog 加载表流程',cs))

    st.append(Paragraph('2.4 Filter 下推三级分类',h2))
    st.append(Paragraph('SparkScanBuilder.pushPredicates() 实现三级过滤分类：',bs))
    st.append(mt([['分类','条件','处理'],
        ['完全下推(A)','可转换 + 选择完整分区','仅 Iceberg 评估, Spark 不再过滤'],
        ['部分下推(B)','可转换 + 不选完整分区','Iceberg 文件裁剪 + Spark 行级过滤'],
        ['不可下推(C)','无法转换或绑定失败','完全由 Spark 评估'],
        ['filterExpressions','A + B 集合','用于 Iceberg scan.filter()'],
        ['postScanFilters','B + C 集合','返回 Spark 做后续过滤']
    ],[90,140,240],C['g']))
    st.append(Paragraph('图 2-4: Filter 下推分类',cs))

    st.append(Paragraph('2.5 Actions 维护操作一览',h2))
    st.append(mt([['Action','功能','核心流程'],
        ['rewriteDataFiles','数据压缩','扫描->分组(BinPack/Sort/ZOrder)->并行重写->提交'],
        ['rewriteManifests','Manifest重写','读取所有Manifest->Spark并行重写->替换'],
        ['expireSnapshots','过期快照清理','确定过期快照->收集文件->Spark并行删除'],
        ['deleteOrphanFiles','孤儿文件清理','列出实际文件-列出引用文件->差集->删除'],
        ['rewritePositionDeletes','Delete文件重写','扫描Position Delete->合并重写->提交'],
        ['computeTableStats','计算统计','ThetaSketch 计算 NDV->写入 Puffin 文件'],
        ['migrateTable','表迁移','创建Iceberg表->导入文件->更新Catalog'],
        ['snapshotTable','表快照','创建新表->导入源表文件->独立管理']
    ],[100,90,280],C['o']))
    st.append(Paragraph('图 2-5: Actions 维护操作',cs))
    st.append(PageBreak())

    # 第三章
    st.append(Paragraph('第三章  核心时序图',h1))
    st.append(Paragraph('3.1 Spark BatchRead 时序',h2))
    st.append(mt([['序号','调用方','\u2192 接收方','操作'],
        ['1','Spark SQL','\u2192 SparkCatalog','loadTable(ident)'],
        ['2','SparkCatalog','\u2192 IcebergCatalog','loadTable(TableIdentifier)'],
        ['3','Spark SQL','\u2192 SparkTable','newScanBuilder(options)'],
        ['4','Spark SQL','\u2192 SparkScanBuilder','pushPredicates/pruneColumns/pushAgg/pushLimit'],
        ['5','SparkScanBuilder','\u2192 SparkV2Filters','convert(predicate) 逐个转换'],
        ['6','SparkScanBuilder','\u2192 IcebergTable','newBatchScan().filter().project()'],
        ['7','Spark SQL','\u2192 SparkScanBuilder','build() -> SparkBatchQueryScan'],
        ['8','SparkBatchQueryScan','\u2192 IcebergScan','planTasks() 规划扫描任务组'],
        ['9','SparkBatch','\u2192 Executors','planInputPartitions() 分配任务'],
        ['10','Executor','\u2192 RowDataReader','read() + DeleteFilter 过滤'],
        ['11','RowDataReader','\u2192 Spark','return Iterator[InternalRow]']
    ],[30,100,80,260],C['b']))
    st.append(Paragraph('图 3-1: BatchRead 时序',cs))

    st.append(Paragraph('3.2 Spark BatchWrite 时序',h2))
    st.append(mt([['序号','调用方','\u2192 接收方','操作'],
        ['1','Spark SQL','\u2192 SparkTable','newWriteBuilder(info)'],
        ['2','Spark SQL','\u2192 SparkWriteBuilder','overwrite()/overwriteDynamic()'],
        ['3','SparkWriteBuilder','\u2192 Schema','validateOrMergeWriteSchema()'],
        ['4','SparkWriteBuilder','\u2192 Spark SQL','return SparkWrite (重写 toBatch/toStreaming)'],
        ['5','Spark SQL','\u2192 SparkWrite','toBatch() -> BatchAppend/DynamicOverwrite/...'],
        ['6','WriterFactory','\u2192 Executor','createWriter() -> Partitioned/UnpartitionedDataWriter'],
        ['7','Executor','\u2192 DataWriter','write(InternalRow) 逐行写入'],
        ['8','DataWriter','\u2192 RollingWriter','滚动写入, 文件达到 targetSize 自动切分'],
        ['9','Executor','\u2192 Driver','commit() -> TaskCommit(DataFile[])'],
        ['10','Driver','\u2192 IcebergTable','newAppend/newOverwrite().commit()'],
        ['11','IcebergCore','\u2192 MetaStore','OCC CAS 提交新 Snapshot']
    ],[30,100,80,260],C['g']))
    st.append(Paragraph('图 3-2: BatchWrite 时序',cs))

    st.append(Paragraph('3.3 Merge-On-Read 行级操作时序',h2))
    st.append(mt([['序号','调用方','\u2192 接收方','操作'],
        ['1','SparkTable','\u2192 Extensions','newRowLevelOperationBuilder()'],
        ['2','Extensions','\u2192 ScanBuilder','buildMergeOnReadScan() 记住 snapshotId'],
        ['3','Extensions','\u2192 DeltaWriteBuilder','build() -> SparkPositionDeltaWrite'],
        ['4','DeltaWriterFactory','\u2192 Executor','createWriter() -> PositionDeltaWriter'],
        ['5','DeltaWriter','\u2192 DVWriter','DELETE: 生成 DV/PositionDelete 文件'],
        ['6','DeltaWriter','\u2192 DataWriter+Del','UPDATE: 新数据文件+删除标记'],
        ['7','DeltaWriter','\u2192 DataWriter','INSERT: 仅写新数据文件'],
        ['8','Executor','\u2192 Driver','DeltaCommit(dataFiles, deleteFiles)'],
        ['9','Driver','\u2192 RowDelta','newRowDelta().addRows().addDeletes()'],
        ['10','RowDelta','\u2192 RowDelta','validateFromSnapshot() 冲突检测'],
        ['11','RowDelta','\u2192 IcebergCore','commit() 原子提交']
    ],[30,100,80,260],C['pu']))
    st.append(Paragraph('图 3-3: MoR 行级操作时序',cs))

    st.append(Paragraph('3.4 Structured Streaming 微批时序',h2))
    st.append(mt([['序号','调用方','\u2192 接收方','操作'],
        ['1','SparkScan','\u2192 Spark SS','toMicroBatchStream(checkpointLoc)'],
        ['2','Spark SS','\u2192 MicroBatchStream','initialOffset() 获取初始偏移量'],
        ['3','Spark SS','\u2192 MicroBatchStream','latestOffset(start, readLimit)'],
        ['4','MicroBatchStream','\u2192 Table','currentSnapshot() 检查新快照'],
        ['5','MicroBatchStream','\u2192 MicroBatches','generateMicroBatch() 生成微批'],
        ['6','Spark SS','\u2192 MicroBatchStream','planInputPartitions(start, end)'],
        ['7','Executor','\u2192 RowDataReader','读取增量数据文件'],
        ['8','Spark SS','\u2192 StreamingWrite','commit(epochId, messages)'],
        ['9','StreamingWrite','\u2192 Table','newFastAppend/newOverwrite() 提交'],
        ['10','Spark SS','\u2192 Checkpoint','持久化偏移量']
    ],[30,100,80,260],C['te']))
    st.append(Paragraph('图 3-4: Streaming 微批时序',cs))
    st.append(PageBreak())

    # 第四章
    st.append(Paragraph('第四章  核心类设计说明',h1))

    st.append(Paragraph('4.1 SparkCatalog - Catalog 适配层',h2))
    st.append(Paragraph('SparkCatalog 继承 BaseCatalog，实现 Spark TableCatalog/SupportsNamespaces/ViewCatalog，将操作委托给 Iceberg Catalog。',bs))
    st.append(mi([['类层次','SparkCatalog extends BaseCatalog (implements TableCatalog, SupportsNamespaces, ViewCatalog, ProcedureCatalog)'],
        ['核心字段','icebergCatalog, asNamespaceCatalog, asViewCatalog, cacheEnabled, tables(HadoopTables)'],
        ['初始化','解析缓存配置 -> buildIcebergCatalog() -> 可选 CachingCatalog 包装 -> 识别 NamespaceSupport/ViewCatalog'],
        ['表加载','5种标识: PathIdentifier, 正常表名, at_timestamp_xxx, snapshot_id_xxx, branch_xxx/tag_xxx'],
        ['时间旅行','loadTable(ident, version): 按版本号/引用名; loadTable(ident, timestamp): 微秒转毫秒'],
        ['表创建','createTable->SparkTable; stageCreate/stageReplace->StagedSparkTable(Transaction)'],
        ['Alter变更','分类: SetProperty/RemoveProperty/ColumnChange; 拦截 sort-order/identifier-fields; Transaction 原子提交']]))
    st.append(Paragraph('表 4-1: SparkCatalog 设计',cs))

    st.append(Paragraph('4.2 SparkTable - 表抽象层',h2))
    st.append(Paragraph('SparkTable 实现了读/写/删除/行级操作等多个 Spark 接口，是 Iceberg Table 在 Spark 中的表示。',bs))
    st.append(mi([['实现接口','Table, SupportsRead, SupportsWrite, SupportsDeleteV2, SupportsRowLevelOperations, SupportsMetadataColumns'],
        ['核心字段','icebergTable, snapshotId(Long), branch(String), refreshEagerly(bool), isTableRewrite(bool)'],
        ['Capabilities','BATCH_READ, BATCH_WRITE, MICRO_BATCH_READ, STREAMING_WRITE, OVERWRITE_BY_FILTER, OVERWRITE_DYNAMIC'],
        ['元数据列','_spec_id(INT), _partition(STRUCT), _file(STRING), _pos(LONG), _deleted(BOOL), _row_id(LONG), _last_updated_seq'],
        ['读入口','newScanBuilder() -> SparkScanBuilder (传入 branch/snapshotId/schema)'],
        ['写入口','newWriteBuilder() -> SparkWriteBuilder; newRowLevelOperationBuilder()'],
        ['元数据删除','canDeleteWhere(): 检查分区过滤+StrictMetrics; deleteWhere(): deleteFromRowFilter'],
        ['不可变复制','copyWithSnapshotId(long) / copyWithBranch(String) - 时间旅行/分支副本']]))
    st.append(Paragraph('表 4-2: SparkTable 设计',cs))

    st.append(Paragraph('4.3 SparkScanBuilder / SparkScan - 读取体系',h2))
    st.append(Paragraph('采用 Builder 模式，SparkScanBuilder 构建扫描计划，SparkScan 及子类执行扫描。',bs))
    st.append(mt([['类继承关系'],
        ['SparkScan (abstract)\n  \u251c\u2500 SparkPartitioningAwareScan\n  \u2502   \u251c\u2500 SparkBatchQueryScan (+ RuntimeV2Filtering)\n  \u2502   \u2514\u2500 SparkCopyOnWriteScan\n  \u251c\u2500 SparkChangelogScan\n  \u2514\u2500 SparkLocalScan (聚合下推本地扫描)']
    ],[480]))
    st.append(Paragraph('图 4-1: Scan 类继承体系',cs))
    st.append(mt([['组件','核心职责'],
        ['SparkScanBuilder','pushPredicates() 三级分类; pruneColumns() 列裁剪; pushAggregation() 聚合下推; pushLimit(); build()'],
        ['SparkScan','toBatch()->SparkBatch; toMicroBatchStream(); estimateStatistics(含NDV/CBO); 30+自定义Metrics'],
        ['SparkBatchQueryScan','运行时过滤(SupportsRuntimeV2Filtering); filterAttributes()暴露分区字段; rewritableDeletes()'],
        ['SparkCopyOnWriteScan','COW 行级操作专用, 记录受影响文件'],
        ['SparkChangelogScan','CDC 变更日志扫描, 支持时间/快照范围'],
        ['SparkLocalScan','聚合下推后本地扫描(无需读文件)']
    ],[110,360],C['b']))
    st.append(Paragraph('表 4-3: Scan 体系职责',cs))
    st.append(PageBreak())

    st.append(Paragraph('4.4 SparkWrite / SparkWriteBuilder - 写入体系',h2))
    st.append(mt([['SparkWrite 写入模式体系'],
        ['SparkWrite (abstract)\n  \u251c\u2500 BaseBatchWrite\n  \u2502   \u251c\u2500 BatchAppend (INSERT INTO)\n  \u2502   \u251c\u2500 DynamicOverwrite (动态分区覆写)\n  \u2502   \u251c\u2500 OverwriteByFilter (条件覆写)\n  \u2502   \u251c\u2500 CopyOnWriteOperation (COW)\n  \u2502   \u2514\u2500 RewriteFiles (压缩)\n  \u2514\u2500 BaseStreamingWrite\n      \u251c\u2500 StreamingAppend\n      \u2514\u2500 StreamingOverwrite']
    ],[480]))
    st.append(Paragraph('图 4-2: SparkWrite 模式体系',cs))
    st.append(mt([['组件','核心设计'],
        ['SparkWriteBuilder','确定模式(append/overwrite/dynamic/cow); validateOrMergeWriteSchema(); 行血统(Row Lineage)注入'],
        ['WriterFactory','序列化 Table(SerializableTableWithSize) -> Broadcast 广播; createWriter()创建对应Writer'],
        ['Unpartitioned','RollingDataWriter: 达到targetFileSize自动切分新文件'],
        ['Partitioned','计算PartitionKey(InternalRowWrapper); fanout->FanoutDataWriter; !fanout->ClusteredDataWriter'],
        ['BatchAppend','table.newAppend() -> appendFile() -> commitOperation()'],
        ['DynamicOverwrite','table.newReplacePartitions(); 支持SERIALIZABLE/SNAPSHOT隔离级别冲突检测'],
        ['CopyOnWrite','收集overwrittenFiles+danglingDVs; newOverwrite().deleteFiles()+addFile(); 冲突检测'],
        ['WAP支持','Write-Audit-Publish: STAGED_WAP_ID_PROP+stageOnly(); 暂存快照不影响当前指针'],
        ['Streaming','幂等提交: queryId+epochId去重; findLastCommittedEpochId()检查历史']
    ],[90,380],C['g']))
    st.append(Paragraph('表 4-4: Write 体系设计',cs))

    st.append(Paragraph('4.5 SparkPositionDeltaWrite - MoR 行级操作',h2))
    st.append(mi([['实现接口','DeltaWrite, RequiresDistributionAndOrdering'],
        ['命令支持','DELETE(仅Delete文件), UPDATE(Delete+新数据), MERGE(Insert+Update+Delete组合)'],
        ['DV支持','启用DV: PartitioningDVWriter生成紧凑DV文件; 否则: ClusteredPositionDeleteWriter'],
        ['Writer类型','BasePositionDeltaWriter(insert/update/delete), FanoutPositionOnlyDeleteWriter, PartitioningDVWriter'],
        ['冲突检测','validateFromSnapshot(scanSnapshotId); SERIALIZABLE:noConflictingData+Deletes; SNAPSHOT:noConflictingDeletes'],
        ['提交','Driver收集DeltaCommit(dataFiles,deleteFiles) -> RowDelta原子提交']]))
    st.append(Paragraph('表 4-5: SparkPositionDeltaWrite 设计',cs))

    st.append(Paragraph('4.6 SparkActions - 维护操作体系',h2))
    st.append(mt([['类继承体系'],
        ['SparkActions implements ActionsProvider\n  \u251c\u2500 BaseSparkAction\n  \u2502   \u251c\u2500 BaseSnapshotUpdateSparkAction\n  \u2502   \u2502   \u251c\u2500 RewriteDataFilesSparkAction\n  \u2502   \u2502   \u251c\u2500 RewriteManifestsSparkAction\n  \u2502   \u2502   \u2514\u2500 RewritePositionDeleteFilesSparkAction\n  \u2502   \u251c\u2500 ExpireSnapshotsSparkAction\n  \u2502   \u2514\u2500 DeleteOrphanFilesSparkAction\n  \u2514\u2500 BaseTableCreationSparkAction\n      \u251c\u2500 MigrateTableSparkAction\n      \u2514\u2500 SnapshotTableSparkAction']
    ],[480]))
    st.append(Paragraph('图 4-3: Actions 类继承体系',cs))
    st.append(mt([['压缩策略','说明'],['BinPack(默认)','按文件大小合并小文件'],['Sort','按排序键重写, 优化数据跳过'],
        ['ZOrder','Z-Order空间曲线排序, 优化多维查询'],['并行策略','MAX_CONCURRENT控制并发; PARTIAL_PROGRESS部分提交']
    ],[120,350],C['pu']))
    st.append(Paragraph('表 4-6: 压缩策略',cs))
    st.append(PageBreak())

    st.append(Paragraph('4.7 SparkProcedures - 存储过程体系',h2))
    st.append(Paragraph('通过注册表模式管理 20 个存储过程, 用户可通过 CALL catalog.procedure_name(...) 调用。',bs))
    st.append(mt([['存储过程','功能'],['rollback_to_snapshot','回滚到指定快照'],['rollback_to_timestamp','回滚到指定时间戳'],
        ['set_current_snapshot','设置当前快照'],['cherrypick_snapshot','Cherry-pick快照'],
        ['rewrite_data_files','数据文件压缩'],['rewrite_manifests','Manifest重写'],
        ['remove_orphan_files','清理孤儿文件'],['expire_snapshots','过期快照清理'],
        ['migrate','Hive迁移到Iceberg'],['snapshot','创建表快照'],['add_files','添加外部文件'],
        ['register_table','注册表'],['publish_changes','发布WAP暂存变更'],
        ['create_changelog_view','创建CDC视图'],['fast_forward','快进分支'],
        ['rewrite_position_delete_files','重写Position Delete'],
        ['compute_table_stats','计算表统计(NDV)'],['compute_partition_stats','计算分区统计'],
        ['rewrite_table_path','重写表路径']
    ],[150,320],C['te']))
    st.append(Paragraph('表 4-7: 全部存储过程',cs))

    st.append(Paragraph('4.8 SparkV2Filters - 谓词转换',h2))
    st.append(mt([['类别','操作','转换结果'],
        ['比较','=, <>, <, >, <=, >=','equal, notEqual, lessThan, greaterThan...'],
        ['空值','IS NULL, IS NOT NULL','isNull, notNull'],
        ['NaN','IS NaN, IS NOT NaN','isNaN, notNaN'],
        ['集合','IN, NOT IN','in, notIn'],
        ['字符串','STARTS_WITH','startsWith'],
        ['逻辑','AND, OR, NOT','and, or, not'],
        ['分区变换','years/months/days/hours\nbucket/truncate','对应Iceberg分区变换函数']
    ],[60,130,280],C['b']))
    st.append(Paragraph('表 4-8: SparkV2Filters 转换操作',cs))

    st.append(Paragraph('4.9 IcebergSparkSessionExtensions - SQL 扩展',h2))
    st.append(Paragraph('通过 spark.sql.extensions 配置启用, 注入解析器/分析规则/优化规则/执行策略。',bs))
    st.append(mt([['扩展类型','组件','功能'],
        ['Parser','IcebergSparkSqlExtensions\nParser','ANTLR语法: CALL, ALTER TABLE\n(PARTITION/BRANCH/TAG), VIEW'],
        ['Analyzer','ResolveProcedures\nResolveViews\nResolveMergeIntoTable','解析存储过程/视图/MERGE引用\n检查条件/对齐赋值'],
        ['Rewrite','RewriteUpdateTable\nRewriteMergeIntoTable\n*ForRowLineage','重写UPDATE/MERGE为\nIceberg特定逻辑计划\n支持行血统'],
        ['Optimizer','ExtendedSimplify*\nReplaceStaticInvoke\nRemoveRowLineageOutput','谓词简化/Null替换\n静态调用替换\n移除冗余行血统输出'],
        ['Pre-CBO','RowLevelCommandScan*\nExtendedV2Writes\nDynamicPruning','扫描下推/V2写入规则\n动态裁剪/替换重写命令'],
        ['Planner','ExtendedDataSourceV2\nStrategy','逻辑计划->物理Exec节点\nDDL/DML/Procedure映射']
    ],[65,125,280],C['pu']))
    st.append(Paragraph('表 4-9: Extensions 全部扩展',cs))
    st.append(PageBreak())

    # 第五章
    st.append(Paragraph('第五章  关键设计模式总结',h1))
    st.append(mt([['序号','设计模式','应用场景','关键实现'],
        ['1','Builder 模式','扫描/写入构建','SparkScanBuilder/SparkWriteBuilder: 逐步设置后build()'],
        ['2','模板方法','写入提交流程','SparkWrite.commitOperation()通用逻辑; 子类实现具体commit()'],
        ['3','适配器模式','DSv2 API 对接','SparkCatalog/SparkTable/SparkV2Filters 三层适配'],
        ['4','策略模式','压缩/写入/删除','BinPack/Sort/ZOrder; Clustered/Fanout; DV/PositionDelete'],
        ['5','工厂模式','Reader/Writer','WriterFactory/SparkFileWriterFactory/SparkProcedures.newBuilder()'],
        ['6','注册表模式','过程/函数管理','SparkProcedures(20个); SparkFunctions(10个); SPI注册'],
        ['7','广播+序列化','Driver-Executor','SerializableTableWithSize; Broadcast[Table]; SparkInputPartition'],
        ['8','OCC 并发控制','并发写入','SERIALIZABLE/SNAPSHOT隔离; validateFromSnapshot; conflictDetectionFilter'],
        ['9','WAP 发布','安全发布','stageOnly()暂存; publish_changes发布; 不影响当前指针'],
        ['10','Refinement','不可变扫描','copyWithSnapshotId/copyWithBranch; ScanBuilder每次build()独立'],
        ['11','SPI 注册','数据源发现','IcebergSource: DataSourceRegister; META-INF/services SPI'],
        ['12','委托模式','Catalog 分层','SparkCatalog 委托 icebergCatalog; SparkTable 委托 icebergTable']
    ],[30,75,80,285],C['p']))
    st.append(Paragraph('表 5-1: 关键设计模式总结',cs))
    st.append(Spacer(1,20))

    st.append(Paragraph('本文档基于 Apache Iceberg v1.9.2 源码分析生成，涵盖 Spark v3.4 集成模块的整体架构、'
        '核心流程图（查询/写入/Catalog/Filter/Actions）、核心时序图（BatchRead/BatchWrite/MoR/Streaming）、'
        '9 大核心类设计说明以及 12 种关键设计模式。',
        ParagraphStyle('end',parent=bs,textColor=C['tl'],fontSize=9,alignment=TA_CENTER)))

    doc.build(st)
    print(f"PDF generated: {op}")
    return op

if __name__=='__main__':
    build()
