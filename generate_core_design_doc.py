#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Apache Iceberg Core 模块源码设计文档生成器"""

from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import mm
from reportlab.lib.colors import HexColor, black, white, grey, lightgrey, darkgoldenrod
from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_JUSTIFY
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, PageBreak, Table, TableStyle,
    HRFlowable, Flowable
)
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
import os, platform

# === 字体注册 ===
def register_fonts():
    system = platform.system()
    paths = []
    if system == 'Darwin':
        paths = ['/System/Library/Fonts/STHeiti Light.ttc', '/System/Library/Fonts/PingFang.ttc',
                 '/Library/Fonts/Arial Unicode.ttf', '/System/Library/Fonts/Hiragino Sans GB.ttc',
                 '/System/Library/Fonts/Supplemental/Songti.ttc']
    elif system == 'Linux':
        paths = ['/usr/share/fonts/truetype/wqy/wqy-zenhei.ttc', '/usr/share/fonts/truetype/wqy/wqy-microhei.ttc']
    for p in paths:
        if os.path.exists(p):
            try:
                pdfmetrics.registerFont(TTFont('CF', p))
                return True
            except: continue
    return False

HCF = register_fonts()
BF = 'CF' if HCF else 'Helvetica'
CF = 'Courier'

# === 颜色 ===
IB = HexColor('#0066CC')
ID = HexColor('#003366')
IL = HexColor('#E6F0FF')
TH_BG = HexColor('#2c3e50')
ALT_ROW = HexColor('#f8f9fa')

styles = getSampleStyleSheet()

def S(name, parent='Normal', **kw):
    defaults = {'fontName': BF}
    defaults.update(kw)
    return ParagraphStyle(name, parent=styles[parent], **defaults)

ct = S('ct', 'Title', fontSize=28, leading=36, textColor=ID, alignment=TA_CENTER, spaceAfter=10)
cs = S('cs', fontSize=14, leading=20, textColor=grey, alignment=TA_CENTER, spaceAfter=6)
h1 = S('h1', 'Heading1', fontSize=20, leading=26, textColor=ID, spaceBefore=20, spaceAfter=12)
h2 = S('h2', 'Heading2', fontSize=16, leading=22, textColor=IB, spaceBefore=14, spaceAfter=8)
h3 = S('h3', 'Heading3', fontSize=13, leading=18, textColor=HexColor('#2c5282'), spaceBefore=10, spaceAfter=6)
bd = S('bd', fontSize=10, leading=16, alignment=TA_JUSTIFY, spaceBefore=3, spaceAfter=3)
cap = S('cap', fontSize=9, leading=13, textColor=grey, alignment=TA_CENTER, spaceBefore=4, spaceAfter=10)
ts = S('ts', fontSize=11, leading=20, textColor=ID, spaceBefore=2, spaceAfter=2)
tss = S('tss', fontSize=10, leading=18, textColor=HexColor('#555555'), spaceBefore=1, spaceAfter=1, leftIndent=20)

def mk_table(headers, rows, cw=None):
    hp = [Paragraph(f'<b>{h}</b>', S('_th', fontSize=9, textColor=white)) for h in headers]
    data = [hp] + [[Paragraph(str(c), S('_td', fontSize=8, leading=12)) for c in r] for r in rows]
    if not cw: cw = [460/len(headers)] * len(headers)
    t = Table(data, colWidths=cw)
    sc = [('BACKGROUND',(0,0),(-1,0),TH_BG),('TEXTCOLOR',(0,0),(-1,0),white),
          ('FONTNAME',(0,0),(-1,0),BF),('FONTSIZE',(0,0),(-1,0),9),
          ('ALIGN',(0,0),(-1,0),'CENTER'),('VALIGN',(0,0),(-1,-1),'MIDDLE'),
          ('GRID',(0,0),(-1,-1),0.5,HexColor('#d1d5db')),
          ('TOPPADDING',(0,0),(-1,-1),5),('BOTTOMPADDING',(0,0),(-1,-1),5),
          ('LEFTPADDING',(0,0),(-1,-1),6),('RIGHTPADDING',(0,0),(-1,-1),6)]
    for i in range(1,len(data)):
        if i%2==0: sc.append(('BACKGROUND',(0,i),(-1,i),ALT_ROW))
    t.setStyle(TableStyle(sc))
    return t

def mk_box(text, bg=IL, border=IB, w=460):
    data = [[Paragraph(text, S('_bx', fontSize=9, leading=14))]]
    t = Table(data, colWidths=[w])
    t.setStyle(TableStyle([('BACKGROUND',(0,0),(-1,-1),bg),('BOX',(0,0),(-1,-1),1,border),
                           ('LEFTPADDING',(0,0),(-1,-1),10),('RIGHTPADDING',(0,0),(-1,-1),10),
                           ('TOPPADDING',(0,0),(-1,-1),8),('BOTTOMPADDING',(0,0),(-1,-1),8)]))
    return t

# === 流程图 ===
class FlowChart(Flowable):
    def __init__(self, steps, width=480, bh=32, gap=18, title=""):
        Flowable.__init__(self)
        self.steps, self.chart_width, self.bh, self.gap, self.title = steps, width, bh, gap, title
        self.width = width
        self.height = len(steps) * (bh + gap) + 30

    def draw(self):
        c = self.canv; y = self.height - 20
        if self.title:
            c.setFont(BF, 11); c.setFillColor(ID); c.drawCentredString(self.chart_width/2, y, self.title); y -= 20
        for i, s in enumerate(self.steps):
            bx, bw, by = 60, self.chart_width-120, y-self.bh
            c.setStrokeColor(s.get('border', HexColor('#3b82f6'))); c.setLineWidth(1.2)
            c.setFillColor(s.get('color', HexColor('#dbeafe')))
            if s.get('type') in ('start','end'): c.roundRect(bx, by, bw, self.bh, 14, fill=1, stroke=1)
            else: c.roundRect(bx, by, bw, self.bh, 6, fill=1, stroke=1)
            c.setFillColor(black); c.setFont(BF, 9)
            c.drawCentredString(bx+bw/2, by+self.bh/2-4, s.get('text',''))
            if i < len(self.steps)-1:
                ax = bx+bw/2; c.setStrokeColor(grey); c.setLineWidth(1)
                c.line(ax, by, ax, by-self.gap+5)
                c.setFillColor(grey); p = c.beginPath()
                p.moveTo(ax-4, by-self.gap+7); p.lineTo(ax, by-self.gap); p.lineTo(ax+4, by-self.gap+7); p.close()
                c.drawPath(p, fill=1, stroke=0)
            y -= (self.bh + self.gap)

# === 时序图 ===
class SeqDiagram(Flowable):
    def __init__(self, actors, msgs, width=500, title=""):
        Flowable.__init__(self)
        self.actors, self.msgs, self.title, self.width = actors, msgs, title, width
        self.mg = 30
        self.height = 40 + len(msgs)*self.mg + 40

    def _ax(self, idx):
        n = len(self.actors); sp = (self.width-40)/max(n-1,1) if n>1 else self.width/2
        return 20 + idx*sp

    def draw(self):
        c = self.canv; top = self.height; bw, bh = 72, 24
        if self.title:
            c.setFont(BF, 10); c.setFillColor(ID); c.drawCentredString(self.width/2, top-12, self.title); top -= 18
        for i, a in enumerate(self.actors):
            ax = self._ax(i); bx = ax-bw/2; by = top-bh
            c.setFillColor(HexColor('#fef3c7')); c.setStrokeColor(darkgoldenrod); c.setLineWidth(1)
            c.roundRect(bx, by, bw, bh, 4, fill=1, stroke=1)
            c.setFillColor(black); c.setFont(BF, 7); c.drawCentredString(ax, by+7, a)
        lt, lb = top-bh, top-bh-len(self.msgs)*self.mg-15
        c.setStrokeColor(lightgrey); c.setLineWidth(0.5); c.setDash(3,3)
        for i in range(len(self.actors)): c.line(self._ax(i), lt, self._ax(i), lb)
        c.setDash()
        my = lt - 18
        for (fi, ti, txt, st) in self.msgs:
            fx, tx = self._ax(fi), self._ax(ti)
            if st == 'self':
                c.setStrokeColor(HexColor('#1e40af')); c.setLineWidth(1); c.setDash()
                c.line(fx, my, fx+25, my); c.line(fx+25, my, fx+25, my-10); c.line(fx+25, my-10, fx+5, my-10)
                c.setFillColor(HexColor('#374151')); c.setFont(BF, 6); c.drawString(fx+28, my-6, txt)
                my -= self.mg; continue
            if st == 'dashed': c.setStrokeColor(HexColor('#6b7280')); c.setLineWidth(1); c.setDash(4,3)
            else: c.setStrokeColor(HexColor('#1e40af')); c.setLineWidth(1.2); c.setDash()
            c.line(fx, my, tx, my)
            d = 1 if tx>fx else -1
            c.setFillColor(HexColor('#1e40af') if st=='solid' else HexColor('#6b7280'))
            p = c.beginPath(); p.moveTo(tx, my); p.lineTo(tx-d*7, my+4); p.lineTo(tx-d*7, my-4); p.close()
            c.drawPath(p, fill=1, stroke=0)
            c.setFillColor(HexColor('#374151')); c.setFont(BF, 6)
            c.drawCentredString((fx+tx)/2, my+5, txt)
            my -= self.mg
        c.setDash()

# === 类图 ===
class ClassDiag(Flowable):
    def __init__(self, classes, rels, width=500, title=""):
        Flowable.__init__(self)
        self.classes, self.rels, self.title, self.width = classes, rels, title, width
        self.height = max(cl[1] for cl in classes)+60 if classes else 100

    def draw(self):
        c = self.canv; bw, bh = 100, 28; positions = []
        if self.title:
            c.setFont(BF, 10); c.setFillColor(ID); c.drawCentredString(self.width/2, self.height-12, self.title)
        for (x, y, name, ct2, color) in self.classes:
            ry = self.height-y-30
            c.setFillColor(color); c.setStrokeColor(HexColor('#4a5568')); c.setLineWidth(1)
            if ct2=='interface': c.setDash(3,2)
            else: c.setDash()
            c.roundRect(x, ry, bw, bh, 5, fill=1, stroke=1); c.setDash()
            c.setFillColor(black); c.setFont(BF, 7)
            if ct2 in ('interface','abstract'):
                c.drawCentredString(x+bw/2, ry+bh/2+2, f"<<{ct2}>>")
                c.setFont(BF, 8); c.drawCentredString(x+bw/2, ry+bh/2-9, name)
            else:
                c.setFont(BF, 8); c.drawCentredString(x+bw/2, ry+bh/2-4, name)
            positions.append((x+bw/2, ry+bh/2, x, ry, bw, bh))
        for (fi, ti, lbl, lt2) in self.rels:
            if fi>=len(positions) or ti>=len(positions): continue
            fcx,fcy,fx,fy,fw,fh = positions[fi]; tcx,tcy,tx,ty,tw,th = positions[ti]
            sy = fy if fcy>tcy else fy+fh; ey = ty+th if fcy>tcy else ty
            c.setStrokeColor(HexColor('#6b7280')); c.setLineWidth(0.8)
            if lt2=='implements': c.setDash(4,3)
            else: c.setDash()
            c.line(fcx, sy, tcx, ey); c.setDash()
            d = 1 if sy>ey else -1
            c.setFillColor(white)
            p = c.beginPath(); p.moveTo(tcx, ey); p.lineTo(tcx-5, ey+d*8); p.lineTo(tcx+5, ey+d*8); p.close()
            c.drawPath(p, fill=1, stroke=1)

def add_pn(cv, doc):
    cv.saveState()
    cv.setFont(BF, 8); cv.setFillColor(grey); cv.drawCentredString(A4[0]/2, 20*mm, f"- {doc.page} -")
    cv.setStrokeColor(IB); cv.setLineWidth(0.5); cv.line(25*mm, A4[1]-18*mm, A4[0]-25*mm, A4[1]-18*mm)
    cv.setFont(BF, 7); cv.setFillColor(IB)
    cv.drawString(25*mm, A4[1]-16*mm, "Apache Iceberg Core"); cv.drawRightString(A4[0]-25*mm, A4[1]-16*mm, "v1.9.2")
    cv.restoreState()

# ========== 文档构建 ==========
def build():
    out = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'Iceberg_Core_Design_Document.pdf')
    doc = SimpleDocTemplate(out, pagesize=A4, topMargin=25*mm, bottomMargin=25*mm, leftMargin=25*mm, rightMargin=25*mm,
                            title="Apache Iceberg Core 模块设计文档", author="Iceberg Source Analysis")
    story = []

    # 封面
    story.append(Spacer(1, 60))
    story.append(Paragraph("Apache Iceberg", ct))
    story.append(Paragraph("Core 模块源码设计文档", S('_ct2', 'Title', fontSize=22, leading=30, textColor=IB, alignment=TA_CENTER)))
    story.append(Spacer(1, 20))
    story.append(HRFlowable(width="60%", thickness=2, color=IB, spaceAfter=20))
    story.append(Paragraph("版本: 1.9.2  |  核心流程图 / 时序图 / 类设计说明", cs))
    story.append(Spacer(1, 30))
    story.append(Paragraph("Apache Iceberg 是高性能的开放表格式(Open Table Format)，专为超大规模分析型数据集设计。Core 模块是核心引擎，提供表元数据管理、快照机制、Manifest 文件组织、扫描规划、事务控制和 Catalog 抽象等关键功能。本文档基于 v1.9.2 源码深度分析。", S('_intro', fontSize=10, leading=18, alignment=TA_CENTER, textColor=HexColor('#555555'))))
    story.append(PageBreak())

    # 目录
    story.append(Paragraph("目  录", h1))
    story.append(Spacer(1, 10))
    for item, sub in [("第一章  Iceberg Core 整体架构概览",0),("    1.1 模块分层架构",1),("    1.2 核心包结构",1),("    1.3 数据文件组织模型",1),
                      ("第二章  核心流程图",0),("    2.1 数据写入提交流程",1),("    2.2 数据扫描规划流程",1),("    2.3 表元数据更新流程",1),("    2.4 事务提交流程",1),("    2.5 Catalog 加载表流程",1),
                      ("第三章  核心时序图",0),("    3.1 FastAppend 写入时序",1),("    3.2 DataTableScan 扫描时序",1),("    3.3 Transaction 多操作提交时序",1),("    3.4 REST Catalog 表操作时序",1),
                      ("第四章  核心类设计说明",0),("    4.1 TableMetadata",1),("    4.2 SnapshotProducer 体系",1),("    4.3 ManifestGroup 扫描引擎",1),("    4.4 DeleteFileIndex",1),("    4.5 BaseTransaction 事务机制",1),("    4.6 Catalog 体系",1),("    4.7 FileIO/Writer 体系",1),
                      ("第五章  关键设计模式总结",0)]:
        story.append(Paragraph(f'<b>{item}</b>' if not sub else item, ts if not sub else tss))
    story.append(PageBreak())

    # === 第一章 ===
    story.append(Paragraph("第一章  Iceberg Core 整体架构概览", h1))
    story.append(HRFlowable(width="100%", thickness=1.5, color=IB, spaceAfter=12))
    story.append(Paragraph("1.1 模块分层架构", h2))
    story.append(Paragraph("Iceberg Core 模块采用清晰的分层架构设计，从上到下分为 API 层、核心实现层、存储抽象层和序列化层。Core 模块是引擎无关的(Engine-agnostic)，不依赖任何特定计算引擎(Spark/Flink)。", bd))
    story.append(mk_table(['分层','核心职责','关键类/包'],
        [['API 层 (api/)','定义公共接口和类型','Table, Catalog, Schema, PartitionSpec, Scan 等接口'],
         ['核心实现层 (core/)','表规范的完整实现','TableMetadata, SnapshotProducer, ManifestGroup, BaseTransaction'],
         ['Catalog 层','Catalog 服务的多种实现','RESTSessionCatalog, HadoopCatalog, JdbcCatalog, CachingCatalog'],
         ['存储抽象层 (core/io/)','统一的文件 IO 接口和写入框架','FileIO, HadoopFileIO, ResolvingFileIO, BaseTaskWriter'],
         ['序列化层 (core/avro/)','Avro 格式读写，元数据序列化','Avro, ManifestWriter, ManifestReader, TableMetadataParser']],
        [70, 150, 240]))

    story.append(Paragraph("1.2 核心包结构", h2))
    story.append(mk_table(['包名','文件数','核心功能'],
        [['org.apache.iceberg (根包)','~185','表元数据、快照、Manifest、扫描、写操作、事务等核心实现'],
         ['org.apache.iceberg.rest','~92','REST Catalog 完整实现，含 OAuth2、请求/响应模型'],
         ['org.apache.iceberg.avro','~44','Avro 格式读写核心，Schema 转换，值编解码'],
         ['org.apache.iceberg.io','~41','IO 抽象层、任务写入器、滚动写入器、分区写入器'],
         ['org.apache.iceberg.util','~35','工具类集合：Tasks 任务框架、快照工具、线程池等'],
         ['org.apache.iceberg.hadoop','~14','Hadoop 生态集成：FileIO、Catalog、TableOperations'],
         ['org.apache.iceberg.jdbc','~7','JDBC Catalog 实现']],
        [140, 45, 275]))

    story.append(Paragraph("1.3 数据文件组织模型", h2))
    story.append(Paragraph("Iceberg 采用三层文件组织模型：Metadata File -> Manifest List -> Manifest File -> Data/Delete File。每个层级都通过快照(Snapshot)机制实现 MVCC，支持时间旅行和增量读取。", bd))
    story.append(FlowChart([
        {'text':'TableMetadata (v*.metadata.json)','type':'start','color':HexColor('#dbeafe'),'border':HexColor('#2563eb')},
        {'text':'Snapshot (快照: 记录数据某一时刻的完整状态)','color':HexColor('#d1fae5'),'border':HexColor('#059669')},
        {'text':'Manifest List (snap-*.avro: 清单列表文件)','color':HexColor('#fef3c7'),'border':HexColor('#d97706')},
        {'text':'Manifest File (*.avro: 清单文件, 记录数据文件元信息)','color':HexColor('#fed7aa'),'border':HexColor('#ea580c')},
        {'text':'Data Files (Parquet/ORC/Avro) + Delete Files','type':'end','color':HexColor('#e9d5ff'),'border':HexColor('#7c3aed')}],
        title="Iceberg 数据文件组织层次模型"))
    story.append(Paragraph("图 1-1: Iceberg 数据文件的层次组织模型", cap))
    story.append(mk_box("<b>核心设计理念：</b><br/>1. <b>不可变性</b>：TableMetadata/Schema/PartitionSpec 均为不可变对象，通过 Builder 产生新实例<br/>2. <b>MVCC</b>：每次写操作产生新快照，读写不互相阻塞<br/>3. <b>乐观并发</b>：写操作使用 CAS(Compare-And-Swap) 提交<br/>4. <b>Schema Evolution</b>：通过 field ID 而非列名关联数据"))
    story.append(PageBreak())

    # === 第二章 ===
    story.append(Paragraph("第二章  核心流程图", h1))
    story.append(HRFlowable(width="100%", thickness=1.5, color=IB, spaceAfter=12))

    story.append(Paragraph("2.1 数据写入提交流程 (Snapshot Commit)", h2))
    story.append(Paragraph("SnapshotProducer 是所有写操作的基类，其 commit() 方法实现了带重试的乐观并发提交机制。流程包括：生成快照、写入 Manifest、提交元数据更新、冲突检测与重试、清理未提交文件。", bd))
    story.append(FlowChart([
        {'text':'1. 调用 commit() 方法开始提交','type':'start','color':HexColor('#dbeafe'),'border':HexColor('#2563eb')},
        {'text':'2. refresh() 获取最新 TableMetadata','color':HexColor('#dbeafe'),'border':HexColor('#3b82f6')},
        {'text':'3. apply() 生成新快照 - 写入 Manifest 文件','color':HexColor('#dbeafe'),'border':HexColor('#3b82f6')},
        {'text':'4. validate() 执行冲突检测验证','color':HexColor('#fef3c7'),'border':HexColor('#d97706')},
        {'text':'5. 写入 ManifestList 文件 (snap-*.avro)','color':HexColor('#dbeafe'),'border':HexColor('#3b82f6')},
        {'text':'6. 构建新 TableMetadata (Builder 模式)','color':HexColor('#dbeafe'),'border':HexColor('#3b82f6')},
        {'text':'7. TableOperations.commit(base, updated) 原子提交','color':HexColor('#d1fae5'),'border':HexColor('#059669')},
        {'text':'8. 成功:清理未提交 Manifest / 失败:指数退避重试','type':'end','color':HexColor('#e9d5ff'),'border':HexColor('#7c3aed')}],
        title="SnapshotProducer.commit() 数据写入提交流程"))
    story.append(Paragraph("图 2-1: SnapshotProducer.commit() 完整流程", cap))
    story.append(Paragraph("<b>关键机制：</b>乐观重试使用 Tasks.foreach() 框架，默认最多重试 4 次指数退避；validate() 在 apply() 前调用检查冲突；提交后 cleanUncommitted() 删除临时 Manifest。", bd))

    story.append(Paragraph("2.2 数据扫描规划流程 (Scan Planning)", h2))
    story.append(Paragraph("DataTableScan 是最常用的扫描入口，委托 ManifestGroup 进行 Manifest 过滤和文件规划。支持三级过滤：Manifest 级、分区级和文件级。", bd))
    story.append(FlowChart([
        {'text':'1. DataTableScan.doPlanFiles() 开始规划','type':'start','color':HexColor('#dbeafe'),'border':HexColor('#2563eb')},
        {'text':'2. 从 Snapshot 获取 dataManifests + deleteManifests','color':HexColor('#dbeafe'),'border':HexColor('#3b82f6')},
        {'text':'3. 构建 ManifestGroup 并设置过滤条件','color':HexColor('#dbeafe'),'border':HexColor('#3b82f6')},
        {'text':'4. ManifestEvaluator: Manifest 级分区统计过滤','color':HexColor('#fef3c7'),'border':HexColor('#d97706')},
        {'text':'5. Evaluator: 逐条目分区过滤 + 文件统计过滤','color':HexColor('#fed7aa'),'border':HexColor('#ea580c')},
        {'text':'6. DeleteFileIndex: 构建删除文件索引','color':HexColor('#dbeafe'),'border':HexColor('#3b82f6')},
        {'text':'7. 组合数据文件+关联删除文件 -> FileScanTask','color':HexColor('#d1fae5'),'border':HexColor('#059669')},
        {'text':'8. 返回 CloseableIterable<FileScanTask>','type':'end','color':HexColor('#e9d5ff'),'border':HexColor('#7c3aed')}],
        title="DataTableScan 扫描规划流程"))
    story.append(Paragraph("图 2-2: DataTableScan 数据扫描规划完整流程", cap))

    story.append(Paragraph("2.3 表元数据更新流程", h2))
    story.append(FlowChart([
        {'text':'1. 获取当前 TableMetadata','type':'start','color':HexColor('#dbeafe'),'border':HexColor('#2563eb')},
        {'text':'2. TableMetadata.buildFrom(current) 创建 Builder','color':HexColor('#dbeafe'),'border':HexColor('#3b82f6')},
        {'text':'3. Builder 执行变更 (addSnapshot/setSchema/...)','color':HexColor('#fef3c7'),'border':HexColor('#d97706')},
        {'text':'4. Builder.build() 生成新的不可变 TableMetadata','color':HexColor('#dbeafe'),'border':HexColor('#3b82f6')},
        {'text':'5. TableMetadataParser.toJson() 序列化为 JSON','color':HexColor('#dbeafe'),'border':HexColor('#3b82f6')},
        {'text':'6. 写入新 metadata 文件 + 原子更新指针(CAS)','type':'end','color':HexColor('#d1fae5'),'border':HexColor('#059669')}],
        title="TableMetadata 更新流程"))
    story.append(Paragraph("图 2-3: 表元数据更新流程", cap))

    story.append(Paragraph("2.4 事务提交流程", h2))
    story.append(FlowChart([
        {'text':'1. Transaction.newAppend/newOverwrite 创建操作','type':'start','color':HexColor('#dbeafe'),'border':HexColor('#2563eb')},
        {'text':'2. 操作在 TransactionTableOperations 上执行(内存)','color':HexColor('#dbeafe'),'border':HexColor('#3b82f6')},
        {'text':'3. 每个操作 commit() 更新内存中的 current','color':HexColor('#fef3c7'),'border':HexColor('#d97706')},
        {'text':'4. commitTransaction() 检查所有操作已提交','color':HexColor('#dbeafe'),'border':HexColor('#3b82f6')},
        {'text':'5. 带重试的 CAS 提交到真实 TableOperations','color':HexColor('#d1fae5'),'border':HexColor('#059669')},
        {'text':'6. 成功:清理临时文件 / 失败:回滚','type':'end','color':HexColor('#e9d5ff'),'border':HexColor('#7c3aed')}],
        title="Transaction 事务提交流程"))
    story.append(Paragraph("图 2-4: 事务提交流程", cap))

    story.append(Paragraph("2.5 Catalog 加载表流程", h2))
    story.append(FlowChart([
        {'text':'1. Catalog.loadTable(identifier)','type':'start','color':HexColor('#dbeafe'),'border':HexColor('#2563eb')},
        {'text':'2. isValidIdentifier() 验证标识符','color':HexColor('#fef3c7'),'border':HexColor('#d97706')},
        {'text':'3. newTableOps(identifier) 创建 TableOperations','color':HexColor('#dbeafe'),'border':HexColor('#3b82f6')},
        {'text':'4. doRefresh() 加载 + 解析 TableMetadata','color':HexColor('#dbeafe'),'border':HexColor('#3b82f6')},
        {'text':'5. new BaseTable(ops, name, reporter)','color':HexColor('#d1fae5'),'border':HexColor('#059669')},
        {'text':'6. 返回 Table 对象','type':'end','color':HexColor('#e9d5ff'),'border':HexColor('#7c3aed')}],
        title="Catalog 加载表流程"))
    story.append(Paragraph("图 2-5: Catalog 加载表完整流程", cap))
    story.append(PageBreak())

    # === 第三章 ===
    story.append(Paragraph("第三章  核心时序图", h1))
    story.append(HRFlowable(width="100%", thickness=1.5, color=IB, spaceAfter=12))

    story.append(Paragraph("3.1 FastAppend 写入时序", h2))
    story.append(Paragraph("FastAppend 直接追加新 Manifest 文件，不合并已有 Manifest，适用于流式写入和小批量追加。", bd))
    story.append(SeqDiagram(['Client','FastAppend','SnapshotProducer','TableOps','FileIO'],
        [(0,1,'appendFile(dataFile)','solid'),(1,1,'summaryBuilder.addedFile()','self'),
         (0,1,'commit()','solid'),(1,2,'apply()','solid'),(2,2,'refresh() -> base metadata','self'),
         (1,4,'writeNewManifests()','solid'),(4,1,'return manifestFiles','dashed'),
         (2,4,'write ManifestList','solid'),(4,2,'return manifestList path','dashed'),
         (2,2,'build new Snapshot','self'),(2,3,'commit(base, updated)','solid'),
         (3,2,'success / CommitFailedException','dashed'),(2,0,'commit completed','dashed')],
        title="FastAppend 数据追加写入时序图"))
    story.append(Paragraph("图 3-1: FastAppend 数据追加写入时序图", cap))

    story.append(Paragraph("3.2 DataTableScan 扫描时序", h2))
    story.append(SeqDiagram(['Client','DataTableScan','ManifestGroup','ManifestReader','DeleteFileIdx'],
        [(0,1,'planFiles()','solid'),(1,1,'snapshot().dataManifests()','self'),
         (1,2,'new ManifestGroup(io, manifests)','solid'),(1,2,'filterData(expr).select(cols)','solid'),
         (2,4,'deleteIndexBuilder.build()','solid'),(4,2,'return DeleteFileIndex','dashed'),
         (2,3,'ManifestEvaluator 过滤','solid'),(3,2,'过滤后 Manifest 列表','dashed'),
         (2,3,'逐条目分区过滤','solid'),(3,2,'过滤后 Entry 列表','dashed'),
         (2,4,'forDataFile(seq, file)','solid'),(4,2,'关联 DeleteFile[]','dashed'),
         (2,0,'CloseableIterable<FileScanTask>','dashed')],
        title="DataTableScan 扫描规划时序图"))
    story.append(Paragraph("图 3-2: DataTableScan 扫描规划时序图", cap))

    story.append(Paragraph("3.3 Transaction 多操作提交时序", h2))
    story.append(SeqDiagram(['Client','Transaction','TxTableOps','AppendFiles','RealTableOps'],
        [(0,1,'table.newTransaction()','solid'),(0,1,'newAppend()','solid'),
         (1,3,'new MergeAppend(txOps)','solid'),(0,3,'appendFile(file).commit()','solid'),
         (3,2,'commit(base, updated)','solid'),(2,2,'更新内存 current','self'),
         (0,1,'newDelete()','solid'),(0,1,'deleteFile(path).commit()','solid'),
         (1,2,'commit(base, updated)','solid'),(2,2,'更新内存 current','self'),
         (0,1,'commitTransaction()','solid'),(1,4,'commit(start, current)','solid'),
         (4,1,'success','dashed')],
        title="Transaction 多操作提交时序图"))
    story.append(Paragraph("图 3-3: Transaction 多操作事务提交时序图", cap))

    story.append(Paragraph("3.4 REST Catalog 表操作时序", h2))
    story.append(SeqDiagram(['Client','RESTCatalog','HTTPClient','CatalogServer'],
        [(0,1,'loadTable(identifier)','solid'),(1,1,'tableSession()','self'),
         (1,2,'GET /v1/namespaces/ns/tables/t','solid'),(2,3,'HTTP + OAuth2 Token','solid'),
         (3,2,'LoadTableResponse','dashed'),(2,1,'response + config','dashed'),
         (1,1,'build RESTTableOperations','self'),(1,0,'return Table','dashed'),
         (0,1,'table.newAppend().commit()','solid'),(1,2,'POST UpdateTableRequest','solid'),
         (2,3,'HTTP MetadataUpdates','solid'),(3,2,'LoadTableResponse (new)','dashed'),
         (2,1,'commit response','dashed')],
        title="REST Catalog 表加载与提交时序图"))
    story.append(Paragraph("图 3-4: REST Catalog 表加载与提交操作时序图", cap))
    story.append(PageBreak())

    # === 第四章 ===
    story.append(Paragraph("第四章  核心类设计说明", h1))
    story.append(HRFlowable(width="100%", thickness=1.5, color=IB, spaceAfter=12))

    story.append(Paragraph("4.1 TableMetadata - 表元数据核心", h2))
    story.append(Paragraph("TableMetadata (67KB) 是 Iceberg 最核心的数据结构，代表表在某一时刻的完整元数据状态。不可变的 Serializable 对象，所有修改通过内部 Builder 产生新实例。", bd))
    story.append(mk_table(['字段名','类型','说明'],
        [['formatVersion','int','表格式版本 (1/2/3/4)，控制可用特性集'],
         ['uuid','String','表的唯一标识，创建后不变'],
         ['location','String','表数据的根存储路径'],
         ['lastSequenceNumber','long','最后使用的序列号，用于 MVCC 可见性'],
         ['schemas / currentSchemaId','List<Schema>/int','历史 Schema 列表和当前 Schema ID'],
         ['specs / defaultSpecId','List<PartitionSpec>/int','分区规格列表和默认分区规格'],
         ['properties','Map<String,String>','表属性配置(压缩、分割大小等)'],
         ['snapshots','List<Snapshot>','快照列表，每个快照记录一次写操作的结果'],
         ['refs','Map<String,SnapshotRef>','分支和标签引用 (main branch + tags)']],
        [105, 110, 245]))
    story.append(mk_box("<b>设计要点：</b><br/>1. <b>不可变性</b>：所有集合使用 ImmutableList/ImmutableMap<br/>2. <b>版本兼容</b>：formatVersion 控制特性门控，V2+ Row-level Delete，V3+ Row Lineage<br/>3. <b>增量更新</b>：Builder 内部维护 changes 列表，记录 MetadataUpdate 事件"))
    story.append(Spacer(1, 8))

    story.append(Paragraph("4.2 SnapshotProducer - 快照生产者体系", h2))
    story.append(Paragraph("SnapshotProducer 是所有数据写入操作的抽象基类，MergingSnapshotProducer 增加了 Manifest 合并和冲突检测。", bd))
    story.append(ClassDiag(
        [(190,0,'SnapshotUpdate','interface',HexColor('#e0f2fe')),
         (190,55,'SnapshotProducer','abstract',HexColor('#dbeafe')),
         (40,120,'FastAppend','class',HexColor('#d1fae5')),
         (190,120,'MergingSnapshotProducer','abstract',HexColor('#fef3c7')),
         (340,120,'BaseRewriteManifests','class',HexColor('#d1fae5')),
         (40,190,'MergeAppend','class',HexColor('#fed7aa')),
         (150,190,'BaseOverwriteFiles','class',HexColor('#fed7aa')),
         (260,190,'BaseRowDelta','class',HexColor('#fed7aa')),
         (370,190,'StreamingDelete','class',HexColor('#fed7aa'))],
        [(1,0,'','implements'),(2,1,'','extends'),(3,1,'','extends'),(4,1,'','extends'),
         (5,3,'','extends'),(6,3,'','extends'),(7,3,'','extends'),(8,3,'','extends')],
        title="SnapshotProducer 类继承体系"))
    story.append(Paragraph("图 4-1: SnapshotProducer 类继承体系", cap))
    story.append(mk_table(['操作类','operation()','特点'],
        [['FastAppend','append','直接追加 Manifest，不合并，性能最优'],
         ['MergeAppend','append','合并小 Manifest，适合频繁小写入'],
         ['BaseOverwriteFiles','overwrite','按条件覆写，需冲突检测'],
         ['BaseRowDelta','overwrite','同时添加数据文件和删除文件'],
         ['BaseReplacePartitions','overwrite','动态覆写指定分区的数据'],
         ['StreamingDelete','delete','流式删除数据文件'],
         ['BaseRewriteFiles','replace','文件重写(compaction)']],
        [100,70,290]))
    story.append(Spacer(1, 8))

    story.append(Paragraph("4.3 ManifestGroup - 扫描引擎", h2))
    story.append(Paragraph("ManifestGroup (17KB) 是扫描规划的核心引擎，实现三级过滤机制，支持并行扫描。", bd))
    story.append(mk_table(['过滤层级','实现类','过滤依据'],
        [['第一级: Manifest 过滤','ManifestEvaluator','利用 Manifest 分区统计(min/max)跳过整个 Manifest'],
         ['第二级: 分区过滤','Evaluator','利用条目分区值判断是否匹配查询条件'],
         ['第三级: 文件统计过滤','InclusiveMetricsEvaluator','利用文件级 column min/max/null-count 过滤']],
        [100,110,250]))

    story.append(Paragraph("4.4 DeleteFileIndex - 删除文件索引", h2))
    story.append(Paragraph("DeleteFileIndex (32KB) 是 V2 格式的关键组件，支持三种删除：等值删除、位置删除和删除向量(DV)。", bd))
    story.append(mk_table(['索引类型','匹配策略'],
        [['globalDeletes','序列号 > 数据文件序列号的等值删除应用于所有文件'],
         ['eqDeletesByPartition','按分区匹配，序列号大于数据文件的等值删除才生效'],
         ['posDeletesByPartition','按分区匹配，关联同一分区的位置删除文件'],
         ['posDeletesByPath','按数据文件路径精确匹配位置删除文件'],
         ['dvByPath','按数据文件路径精确匹配 Deletion Vector']],
        [130,330]))

    story.append(Paragraph("4.5 BaseTransaction - 事务机制", h2))
    story.append(Paragraph("BaseTransaction (22KB) 实现多操作事务语义，支持四种事务类型。", bd))
    story.append(mk_table(['事务类型','使用场景','提交方式'],
        [['CREATE_TABLE','创建新表','直接 commit(null, metadata)，不可重试'],
         ['REPLACE_TABLE','替换已有表','带重试的 CAS commit'],
         ['CREATE_OR_REPLACE_TABLE','创建或替换表','先替换，失败后创建'],
         ['SIMPLE','普通多操作事务','带重试 CAS，冲突时重新应用操作']],
        [105,140,215]))

    story.append(Paragraph("4.6 Catalog 体系 - 目录服务抽象", h2))
    story.append(ClassDiag(
        [(190,0,'Catalog','interface',HexColor('#e0f2fe')),
         (190,55,'BaseMetastoreCatalog','abstract',HexColor('#dbeafe')),
         (30,120,'HadoopCatalog','class',HexColor('#d1fae5')),
         (150,120,'JdbcCatalog','class',HexColor('#d1fae5')),
         (270,120,'InMemoryCatalog','class',HexColor('#d1fae5')),
         (380,55,'CachingCatalog','class',HexColor('#fef3c7')),
         (30,190,'RESTSessionCatalog','class',HexColor('#fed7aa'))],
        [(1,0,'','implements'),(2,1,'','extends'),(3,1,'','extends'),(4,1,'','extends'),
         (5,0,'wraps','implements'),(6,0,'','implements')],
        title="Catalog 类体系结构"))
    story.append(Paragraph("图 4-2: Catalog 类体系结构", cap))
    story.append(mk_table(['Catalog','存储介质','适用场景'],
        [['HadoopCatalog','HDFS/S3 文件系统','简单部署，无外部依赖'],
         ['JdbcCatalog','RDBMS (MySQL/PG)','已有 RDBMS 环境'],
         ['InMemoryCatalog','内存','单元测试专用'],
         ['RESTSessionCatalog','REST API','生产级多租户环境，支持 OAuth2 和服务端规划'],
         ['CachingCatalog','(装饰器)','为任意 Catalog 添加内存缓存层']],
        [105,110,245]))

    story.append(Paragraph("4.7 FileIO 与 Writer 体系", h2))
    story.append(mk_table(['组件','说明'],
        [['HadoopFileIO','基于 Hadoop FileSystem API，支持 HDFS 和兼容 S3A'],
         ['InMemoryFileIO','内存实现，用于测试'],
         ['ResolvingFileIO','根据 URI scheme 自动委托到对应 FileIO (s3://->S3FileIO)'],
         ['BaseTaskWriter','任务写入器基类(17KB)，管理打开的文件写入器'],
         ['ClusteredWriter','要求输入按分区排序，一次只打开一个分区写入器'],
         ['FanoutDataWriter','同时打开多个分区写入器，适合无序数据'],
         ['RollingFileWriter','单文件超大小限制时自动滚动到新文件'],
         ['OutputFileFactory','生成带分区目录结构的输出文件路径']],
        [110,350]))
    story.append(PageBreak())

    # === 第五章 ===
    story.append(Paragraph("第五章  关键设计模式总结", h1))
    story.append(HRFlowable(width="100%", thickness=1.5, color=IB, spaceAfter=12))
    patterns = [
        ("1. 不可变对象 + Builder 模式", "TableMetadata/Schema/PartitionSpec 均为不可变对象，所有修改通过 Builder 产生新实例。天然线程安全，Builder 内部跟踪 MetadataUpdate 变更事件。"),
        ("2. 乐观并发控制 (OCC)", "所有写操作通过 CAS 机制实现乐观并发。使用 Tasks.foreach() 框架提供指数退避重试(默认 4 次)。失败后重新读取 base 并重新 apply。"),
        ("3. 模板方法模式", "SnapshotProducer 定义 commit 骨架，子类只需实现 apply()/operation()/summary() 等抽象方法。"),
        ("4. Refinement 模式", "TableScan 的 filter()/select() 等返回新的独立扫描对象，状态不会泄漏。确保扫描对象的不可变性和线程安全。"),
        ("5. 三级过滤优化", "ManifestGroup 实现 Manifest 级->分区级->文件统计级三级过滤，层层递进减少扫描数据量。"),
        ("6. 装饰器模式", "CachingCatalog 添加缓存层；EncryptingFileIO 添加加密；ResolvingFileIO 动态委托。提供灵活的功能组合。"),
        ("7. CloseableIterable 统一抽象", "使用 CloseableIterable 而非 Stream 作为惰性集合抽象。确保资源正确关闭(ManifestReader 文件句柄)。"),
        ("8. 序列号驱动的 MVCC", "每个快照分配递增的序列号，删除文件只对序列号更小的数据文件生效。保证读取一致性。"),
        ("9. 自定义序列化", "不使用 Jackson 注解，采用自定义 XxxParser.toJson/fromJson。JSON 键名 kebab-case。"),
    ]
    for title_text, desc in patterns:
        story.append(Paragraph(f'<b>{title_text}</b>', h3))
        story.append(Paragraph(desc, bd))
    
    story.append(Spacer(1, 20))
    story.append(mk_box("<b>总结：</b>Iceberg Core 模块约 500 个 Java 源文件，通过精心设计的分层架构、不可变对象、乐观并发、三级过滤等机制，实现了高性能、高可靠的开放表格式。其核心类 TableMetadata(67KB)、MergingSnapshotProducer(49KB)、SnapshotProducer(33KB)、DeleteFileIndex(32KB)、RESTSessionCatalog(64KB) 共同构成了引擎无关的数据湖基础设施。"))

    doc.build(story, onFirstPage=add_pn, onLaterPages=add_pn)
    print(f"PDF generated: {out}")
    return out

if __name__ == '__main__':
    build()
