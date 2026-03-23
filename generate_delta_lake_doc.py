#!/usr/bin/env /usr/bin/python3
# -*- coding: utf-8 -*-
"""Apache Iceberg Delta Lake Module - Architecture Design Document PDF Generator"""

import os
from fpdf import FPDF

class IcebergPDF(FPDF):
    def header(self):
        if self.page_no() > 1:
            self.set_font('Helvetica', 'I', 8)
            self.set_text_color(150, 150, 150)
            self.cell(0, 8, 'Apache Iceberg Delta Lake Module - Architecture Design Document', align='C')
            self.ln(10)
    
    def footer(self):
        self.set_y(-15)
        self.set_font('Helvetica', 'I', 8)
        self.set_text_color(150, 150, 150)
        self.cell(0, 10, f'Page {self.page_no()}/{{nb}}', align='C')
    
    def chapter_title(self, title):
        self.set_font('Helvetica', 'B', 18)
        self.set_text_color(26, 115, 232)
        self.cell(0, 12, title, new_x="LMARGIN", new_y="NEXT")
        self.set_draw_color(26, 115, 232)
        self.line(self.l_margin, self.get_y(), self.w - self.r_margin, self.get_y())
        self.ln(6)
    
    def section_title(self, title):
        self.set_font('Helvetica', 'B', 14)
        self.set_text_color(25, 103, 210)
        self.cell(0, 10, title, new_x="LMARGIN", new_y="NEXT")
        self.ln(3)
    
    def sub_title(self, title):
        self.set_font('Helvetica', 'B', 12)
        self.set_text_color(32, 33, 36)
        self.cell(0, 8, title, new_x="LMARGIN", new_y="NEXT")
        self.ln(2)
    
    def body_text(self, text):
        self.set_font('Helvetica', '', 10)
        self.set_text_color(32, 33, 36)
        self.multi_cell(0, 6, text)
        self.ln(2)
    
    def bullet(self, text):
        self.set_font('Helvetica', '', 10)
        self.set_text_color(32, 33, 36)
        x = self.get_x()
        self.cell(8)
        self.cell(4, 6, '-')
        self.multi_cell(0, 6, text)
        self.ln(1)
    
    def code_block(self, text):
        self.set_fill_color(241, 243, 244)
        self.set_draw_color(218, 220, 224)
        self.set_font('Courier', '', 7.5)
        self.set_text_color(51, 51, 51)
        x = self.l_margin + 5
        w = self.w - self.l_margin - self.r_margin - 10
        y_start = self.get_y()
        lines = text.split('\n')
        h = len(lines) * 4.5 + 6
        if self.get_y() + h > self.h - self.b_margin:
            self.add_page()
            y_start = self.get_y()
        self.rect(x, y_start, w, h, style='DF')
        self.set_xy(x + 3, y_start + 3)
        for line in lines:
            self.set_x(x + 3)
            self.cell(w - 6, 4.5, line)
            self.ln(4.5)
        self.ln(4)
    
    def colored_box(self, x, y, w, h, r, g, b, text, text_color=(255,255,255), font_size=8):
        self.set_fill_color(r, g, b)
        self.rect(x, y, w, h, style='F')
        self.set_font('Helvetica', 'B', font_size)
        self.set_text_color(*text_color)
        tw = self.get_string_width(text)
        self.set_xy(x + (w - tw)/2, y + (h - font_size*0.35)/2 - 1)
        self.cell(tw, font_size*0.35, text)
    
    def arrow_down(self, x, y, length):
        self.set_draw_color(100, 100, 100)
        self.set_line_width(0.5)
        self.line(x, y, x, y + length)
        self.line(x, y+length, x-2, y+length-4)
        self.line(x, y+length, x+2, y+length-4)
    
    def arrow_right(self, x, y, length):
        self.set_draw_color(100, 100, 100)
        self.set_line_width(0.4)
        self.line(x, y, x + length, y)
        self.line(x+length, y, x+length-3, y-2)
        self.line(x+length, y, x+length-3, y+2)
    
    def table_row(self, data, widths, header=False):
        if header:
            self.set_fill_color(26, 115, 232)
            self.set_text_color(255, 255, 255)
            self.set_font('Helvetica', 'B', 9)
        else:
            self.set_fill_color(248, 249, 250)
            self.set_text_color(32, 33, 36)
            self.set_font('Helvetica', '', 8.5)
        for i, (d, w) in enumerate(zip(data, widths)):
            self.cell(w, 7, d, border=1, fill=True)
        self.ln()


def build_pdf():
    pdf = IcebergPDF()
    pdf.alias_nb_pages()
    pdf.set_auto_page_break(auto=True, margin=20)
    
    # ======================== COVER ========================
    pdf.add_page()
    pdf.ln(40)
    pdf.set_font('Helvetica', 'B', 28)
    pdf.set_text_color(26, 115, 232)
    pdf.cell(0, 15, 'Apache Iceberg Delta Lake', align='C', new_x="LMARGIN", new_y="NEXT")
    pdf.cell(0, 15, 'Module Architecture Design', align='C', new_x="LMARGIN", new_y="NEXT")
    pdf.cell(0, 15, 'Document', align='C', new_x="LMARGIN", new_y="NEXT")
    pdf.ln(5)
    pdf.set_draw_color(26, 115, 232)
    pdf.set_line_width(1)
    cx = pdf.w / 2
    pdf.line(cx - 50, pdf.get_y(), cx + 50, pdf.get_y())
    pdf.ln(10)
    pdf.set_font('Helvetica', '', 13)
    pdf.set_text_color(95, 99, 104)
    pdf.cell(0, 8, 'Delta Lake to Iceberg Table Migration Module', align='C', new_x="LMARGIN", new_y="NEXT")
    pdf.cell(0, 8, 'Architecture / Design Patterns / Call Chain Analysis', align='C', new_x="LMARGIN", new_y="NEXT")
    pdf.ln(25)
    pdf.set_font('Helvetica', '', 11)
    pdf.set_text_color(32, 33, 36)
    info = [('Project:', 'Apache Iceberg 1.9.2'), ('Module:', 'iceberg-delta-lake'),
            ('Type:', 'Architecture Design Document'), ('Date:', '2026-03-23')]
    for label, value in info:
        pdf.set_x(55)
        pdf.set_font('Helvetica', '', 11)
        pdf.set_text_color(95, 99, 104)
        pdf.cell(35, 8, label, align='R')
        pdf.set_font('Helvetica', 'B', 11)
        pdf.set_text_color(32, 33, 36)
        pdf.cell(60, 8, value)
        pdf.ln()
    
    # ======================== TOC ========================
    pdf.add_page()
    pdf.chapter_title('Table of Contents')
    toc = [
        ('1', 'Module Overview'),
        ('  1.1', 'Purpose and Positioning'),
        ('  1.2', 'Source File Overview'),
        ('2', 'Architecture Design'),
        ('  2.1', 'Overall Architecture Diagram'),
        ('  2.2', 'Layer Design Description'),
        ('  2.3', 'Migration Execution Flowchart'),
        ('  2.4', 'Sequence Diagram'),
        ('3', 'Design Pattern Analysis'),
        ('  3.1', 'Builder Pattern (Fluent API)'),
        ('  3.2', 'Visitor Pattern (Type Conversion)'),
        ('  3.3', 'Strategy Pattern (Commit Classification)'),
        ('  3.4', 'Provider / Factory Pattern'),
        ('  3.5', 'Transaction Pattern'),
        ('  3.6', 'Immutable Value Pattern'),
        ('4', 'Core Class Design Details'),
        ('  4.1', 'SnapshotDeltaLakeTable Interface'),
        ('  4.2', 'BaseSnapshotDeltaLakeTableAction'),
        ('  4.3', 'TypeVisitor & TypeToType'),
        ('  4.4', 'MigrationActionsProvider'),
        ('5', 'Key Scenario Call Chains'),
        ('  5.1', 'Complete Snapshot Migration'),
        ('  5.2', 'Initial Version Commit (Fault Tolerance)'),
        ('  5.3', 'VersionLog Incremental Commit'),
        ('  5.4', 'Type System Conversion'),
        ('  5.5', 'Data File Construction'),
        ('  5.6', 'Spark Integration'),
        ('6', 'Summary and Design Merits'),
    ]
    for num, title in toc:
        if num.startswith('  '):
            pdf.set_font('Helvetica', '', 11)
            pdf.set_text_color(95, 99, 104)
            pdf.set_x(25)
        else:
            pdf.set_font('Helvetica', 'B', 12)
            pdf.set_text_color(32, 33, 36)
            pdf.set_x(15)
        pdf.cell(0, 7, f'{num}  {title}', new_x="LMARGIN", new_y="NEXT")
    
    # ======================== CH1: MODULE OVERVIEW ========================
    pdf.add_page()
    pdf.chapter_title('1. Module Overview')
    
    pdf.section_title('1.1 Purpose and Positioning')
    pdf.body_text(
        'The iceberg-delta-lake module is a dedicated migration tool within the Apache Iceberg project ecosystem. '
        'Its core function is to snapshot an existing Delta Lake table and convert it to an Iceberg table, '
        'enabling organizations to seamlessly transition their data lake infrastructure from Delta Lake to Iceberg format.'
    )
    pdf.body_text('Key design goals of this module:')
    pdf.bullet('Zero-Copy Migration: No data files are duplicated. Only Iceberg metadata is created pointing to original Parquet files.')
    pdf.bullet('Version-Faithful Replay: Every Delta Lake version log is replayed one-by-one into corresponding Iceberg snapshots.')
    pdf.bullet('Tag-based Traceability: Each Iceberg snapshot is tagged with Delta version number and timestamp for lineage tracing.')
    pdf.bullet('Transactional Safety: All operations wrapped in a single Iceberg Transaction ensuring atomicity.')
    pdf.bullet('Engine Agnostic Core: Core logic is engine-independent; Spark integration is a thin convenience layer.')
    
    pdf.section_title('1.2 Source File Overview')
    pdf.body_text('The module contains 5 main source files with approximately 600 lines of core logic:')
    
    headers = ['File Name', 'Type', 'Responsibility']
    widths = [60, 22, 88]
    pdf.table_row(headers, widths, header=True)
    rows = [
        ['SnapshotDeltaLakeTable', 'Interface', 'Public API: fluent builder + Result type'],
        ['BaseSnapshotDeltaLake...', 'Class', 'Core: read Delta log, convert schema, replay'],
        ['DeltaLakeDataTypeVisitor', 'Abstract', 'Generic Visitor for Delta type hierarchy'],
        ['DeltaLakeTypeToType', 'Class', 'Visitor impl: Delta -> Iceberg types'],
        ['...ActionsProvider', 'Interface', 'Provider/Factory with Singleton default'],
        ['...SparkIntegration', 'Utility', 'Spark: resolve catalog from SparkSession'],
    ]
    for row in rows:
        pdf.table_row(row, widths)
    pdf.ln(3)
    pdf.set_font('Helvetica', 'I', 9)
    pdf.set_text_color(95, 99, 104)
    pdf.cell(0, 5, 'Table 1: Source Files of the delta-lake Module', align='C', new_x="LMARGIN", new_y="NEXT")
    
    # ======================== CH2: ARCHITECTURE ========================
    pdf.add_page()
    pdf.chapter_title('2. Architecture Design')
    
    pdf.section_title('2.1 Overall Architecture Diagram')
    pdf.body_text('The module follows a clean four-tier layered architecture:')
    
    # Draw architecture diagram
    lm = 20
    bw = 170
    bh = 12
    y = pdf.get_y() + 2
    
    # Layer 1: User Entry
    pdf.set_fill_color(232, 240, 254)
    pdf.set_draw_color(26, 115, 232)
    pdf.rect(lm, y, bw, 28, style='DF')
    pdf.set_font('Helvetica', 'B', 8)
    pdf.set_text_color(26, 115, 232)
    pdf.set_xy(lm+2, y+1)
    pdf.cell(bw-4, 5, 'User Entry Layer')
    pdf.colored_box(lm+5, y+8, 75, bh, 25,103,210, 'ActionsProvider', font_size=7)
    pdf.colored_box(lm+90, y+8, 75, bh, 123,31,162, 'SparkIntegration', font_size=7)
    pdf.arrow_down(lm+bw/2, y+28, 8)
    y += 40
    
    # Layer 2: Interface
    pdf.set_fill_color(252, 232, 230)
    pdf.set_draw_color(234, 67, 53)
    pdf.rect(lm, y, bw, 28, style='DF')
    pdf.set_font('Helvetica', 'B', 8)
    pdf.set_text_color(234, 67, 53)
    pdf.set_xy(lm+2, y+1)
    pdf.cell(bw-4, 5, 'Interface Layer (Action Pattern)')
    pdf.colored_box(lm+5, y+8, 90, bh, 234,67,53, 'SnapshotDeltaLakeTable', font_size=7)
    pdf.colored_box(lm+105, y+8, 60, bh, 197,34,31, 'Action<T,R>', font_size=7)
    pdf.arrow_down(lm+bw/2, y+28, 8)
    y += 40
    
    # Layer 3: Core
    pdf.set_fill_color(230, 244, 234)
    pdf.set_draw_color(52, 168, 83)
    pdf.rect(lm, y, bw, 38, style='DF')
    pdf.set_font('Helvetica', 'B', 8)
    pdf.set_text_color(52, 168, 83)
    pdf.set_xy(lm+2, y+1)
    pdf.cell(bw-4, 5, 'Core Implementation Layer')
    pdf.colored_box(lm+5, y+8, 75, bh, 52,168,83, 'BaseSnapshotAction', font_size=6.5)
    pdf.colored_box(lm+5, y+23, 55, bh, 13,101,45, 'TypeToType', font_size=6.5)
    pdf.colored_box(lm+68, y+23, 60, bh, 13,101,45, 'DataTypeVisitor', font_size=6.5)
    pdf.colored_box(lm+90, y+8, 75, bh, 52,168,83, 'buildDataFile()', font_size=6.5)
    pdf.arrow_down(lm+bw/2, y+38, 8)
    y += 50
    
    # Layer 4: Dependencies
    pdf.set_fill_color(255, 243, 224)
    pdf.set_draw_color(227, 116, 0)
    pdf.rect(lm, y, bw, 38, style='DF')
    pdf.set_font('Helvetica', 'B', 8)
    pdf.set_text_color(227, 116, 0)
    pdf.set_xy(lm+2, y+1)
    pdf.cell(bw-4, 5, 'External Dependencies')
    pdf.colored_box(lm+5, y+8, 50, bh, 255,109,0, 'DeltaLog', font_size=7)
    pdf.colored_box(lm+60, y+8, 50, bh, 255,109,0, 'VersionLog', font_size=7)
    pdf.colored_box(lm+115, y+8, 50, bh, 255,109,0, 'AddFile', font_size=7)
    pdf.colored_box(lm+5, y+23, 50, bh, 26,115,232, 'Transaction', font_size=7)
    pdf.colored_box(lm+60, y+23, 40, bh, 26,115,232, 'Catalog', font_size=7)
    pdf.colored_box(lm+105, y+23, 60, bh, 26,115,232, 'Schema/Spec', font_size=7)
    
    pdf.set_xy(lm, y+42)
    pdf.ln(5)
    pdf.set_font('Helvetica', 'I', 9)
    pdf.set_text_color(95, 99, 104)
    pdf.cell(0, 5, 'Figure 1: Module Architecture', align='C', new_x="LMARGIN", new_y="NEXT")
    
    pdf.section_title('2.2 Layer Design Description')
    pdf.bullet('User Entry Layer: Two entry points - MigrationActionsProvider for programmatic use, SparkIntegration for Spark SQL context. Both create a SnapshotDeltaLakeTable action.')
    pdf.bullet('Interface Layer: SnapshotDeltaLakeTable extends Action<ThisT, R>. Defines fluent builder methods and the execute() contract.')
    pdf.bullet('Core Implementation: BaseSnapshotDeltaLakeTableAction orchestrates schema conversion (via Visitor pattern), version log replay, and transactional commit.')
    pdf.bullet('External Dependencies: Delta Lake Standalone (DeltaLog, VersionLog, AddFile, RemoveFile) for reading Delta metadata; Iceberg Core API (Transaction, Catalog, Schema) for creating the target table.')
    
    # ======================== CH2.3: EXECUTION FLOWCHART ========================
    pdf.add_page()
    pdf.section_title('2.3 Migration Execution Flowchart')
    pdf.body_text('The execute() method follows an 11-step sequential workflow:')
    
    steps = [
        ('1. Validate Parameters', (26, 115, 232)),
        ('2. DeltaLog.update() - Read Latest Snapshot', (255, 109, 0)),
        ('3. Convert Delta Schema to Iceberg Schema', (52, 168, 83)),
        ('4. Extract PartitionSpec from Delta Snapshot', (52, 168, 83)),
        ('5. Create Iceberg Table Transaction', (26, 115, 232)),
        ('6. Set NameMapping Table Properties', (26, 115, 232)),
        ('7. Commit Initial Delta Snapshot', (123, 31, 162)),
        ('8. Iterate Remaining VersionLog Changes', (227, 116, 0)),
        ('9. Classify: AppendFiles / DeleteFiles / OverwriteFiles', (234, 67, 53)),
        ('10. Tag Each Snapshot (version + timestamp)', (13, 101, 45)),
        ('11. Commit Transaction', (26, 115, 232)),
    ]
    
    bw2 = 140
    x0 = (pdf.w - bw2) / 2
    y0 = pdf.get_y()
    for i, (text, color) in enumerate(steps):
        yy = y0 + i * 20
        if yy + 20 > pdf.h - 30:
            pdf.add_page()
            y0 = pdf.get_y() - i * 20
            yy = y0 + i * 20
        pdf.colored_box(x0, yy, bw2, 14, *color, text, font_size=7)
        if i < len(steps) - 1:
            pdf.arrow_down(x0 + bw2/2, yy + 14, 5)
    
    pdf.set_xy(20, y0 + len(steps)*20 + 5)
    pdf.set_font('Helvetica', 'I', 9)
    pdf.set_text_color(95, 99, 104)
    pdf.cell(0, 5, 'Figure 2: Migration Execution Flowchart', align='C', new_x="LMARGIN", new_y="NEXT")
    
    # ======================== CH2.4: SEQUENCE DIAGRAM ========================
    pdf.add_page()
    pdf.section_title('2.4 Sequence Diagram')
    pdf.body_text('Interaction between core participants during execute():')
    
    actors = ['Client', 'BaseSnapshot', 'DeltaLog', 'TypeVisitor', 'Transaction']
    ax = [25, 58, 95, 132, 165]
    aw = 30
    y0 = pdf.get_y() + 3
    
    for i, (name, x) in enumerate(zip(actors, ax)):
        pdf.colored_box(x, y0, aw, 10, 26, 115, 232, name, font_size=5.5)
        pdf.set_draw_color(218, 220, 224)
        pdf.set_line_width(0.3)
        pdf.set_dash_pattern(dash=2, gap=1.5)
        pdf.line(x + aw/2, y0 + 10, x + aw/2, y0 + 195)
        pdf.set_dash_pattern()
    
    msgs = [
        (0, 1, 'execute()'),
        (1, 2, 'DeltaLog.update()'),
        (2, 1, '<< Snapshot'),
        (1, 3, 'visit(schema, TypeToType)'),
        (3, 1, '<< Iceberg Schema'),
        (1, 4, 'newCreateTableTransaction()'),
        (4, 1, '<< Transaction'),
        (1, 4, 'updateProperties(NameMapping)'),
        (1, 2, 'getSnapshotForVersionAsOf(v)'),
        (2, 1, '<< List<AddFile>'),
        (1, 4, 'newAppend().appendFile().commit()'),
        (1, 4, 'manageSnapshots().createTag()'),
        (1, 2, 'getChanges(v+1)'),
        (2, 1, '<< Iterator<VersionLog>'),
        (1, 4, 'newOverwrite/Append/Delete.commit()'),
        (1, 4, 'commitTransaction()'),
        (1, 0, '<< Result{dataFilesCount}'),
    ]
    
    my = y0 + 15
    for src, dst, msg in msgs:
        sx = ax[src] + aw/2
        dx = ax[dst] + aw/2
        is_return = msg.startswith('<<')
        if is_return:
            pdf.set_draw_color(52, 168, 83)
            pdf.set_dash_pattern(dash=2, gap=1)
        else:
            pdf.set_draw_color(100, 100, 100)
            pdf.set_dash_pattern()
        pdf.set_line_width(0.4)
        pdf.line(sx, my, dx, my)
        # arrow head
        if sx < dx:
            pdf.line(dx, my, dx-2.5, my-1.5)
            pdf.line(dx, my, dx-2.5, my+1.5)
        else:
            pdf.line(dx, my, dx+2.5, my-1.5)
            pdf.line(dx, my, dx+2.5, my+1.5)
        pdf.set_dash_pattern()
        
        pdf.set_font('Helvetica', '', 5)
        label = msg.replace('<< ', '') if is_return else msg
        pdf.set_text_color(32, 33, 36)
        tx = min(sx, dx) + 2
        pdf.set_xy(tx, my - 4)
        pdf.cell(abs(dx-sx)-4, 3, label)
        my += 11
    
    pdf.set_xy(20, my + 5)
    pdf.set_font('Helvetica', 'I', 9)
    pdf.set_text_color(95, 99, 104)
    pdf.cell(0, 5, 'Figure 3: Sequence Diagram - execute()', align='C', new_x="LMARGIN", new_y="NEXT")
    
    # ======================== CH3: DESIGN PATTERNS ========================
    pdf.add_page()
    pdf.chapter_title('3. Design Pattern Analysis')
    pdf.body_text('The delta-lake module employs six well-known design patterns, each solving a specific architectural concern.')
    
    pdf.section_title('3.1 Builder Pattern (Fluent API)')
    pdf.body_text(
        'Pattern Intent: Separate construction from representation, enabling step-by-step configuration with method chaining.'
    )
    pdf.body_text(
        'Application: SnapshotDeltaLakeTable defines fluent builder methods where each returns "this", allowing natural chaining:'
    )
    pdf.code_block(
        'snapshotDeltaLakeTable(location)\n'
        '  .as(TableIdentifier.of("db", "table"))\n'
        '  .icebergCatalog(catalog)\n'
        '  .deltaLakeConfiguration(hadoopConf)\n'
        '  .tableProperty("key", "value")\n'
        '  .tableLocation(newLocation)\n'
        '  .execute();'
    )
    pdf.body_text(
        'Benefit: Self-documenting API. The execute() method validates all required parameters via '
        'Preconditions.checkArgument. Optional parameters have sensible defaults.'
    )
    
    pdf.section_title('3.2 Visitor Pattern (Type Conversion)')
    pdf.body_text(
        'Pattern Intent: Perform operations on elements of an object structure without modifying those classes.'
    )
    pdf.body_text(
        'Application: DeltaLakeDataTypeVisitor<T> is an abstract visitor that traverses Delta Lake\'s type tree. '
        'DeltaLakeTypeToType is the concrete visitor that converts each Delta type node into an Iceberg Type.'
    )
    pdf.body_text('Type Mapping Table:')
    
    type_headers = ['Delta Lake Type', 'Iceberg Type']
    type_widths = [60, 60]
    pdf.table_row(type_headers, type_widths, header=True)
    type_mappings = [
        ['BooleanType', 'BooleanType'],
        ['IntegerType / ShortType / ByteType', 'IntegerType'],
        ['LongType', 'LongType'],
        ['FloatType', 'FloatType'],
        ['DoubleType', 'DoubleType'],
        ['StringType', 'StringType'],
        ['DateType', 'DateType'],
        ['TimestampType', 'TimestampType.withZone()'],
        ['DecimalType(precision, scale)', 'DecimalType.of(p, s)'],
        ['BinaryType', 'BinaryType'],
    ]
    for row in type_mappings:
        pdf.table_row(row, type_widths)
    pdf.ln(2)
    pdf.body_text(
        'Benefit: Clean separation of traversal and conversion logic. Adding new Delta types only requires extending atomic(). '
        'Recursive visit() mechanism handles nested types automatically.'
    )
    
    pdf.section_title('3.3 Strategy Pattern (Commit Classification)')
    pdf.body_text(
        'Pattern Intent: Define interchangeable algorithms encapsulated in each commit strategy.'
    )
    pdf.body_text(
        'Application: commitDeltaVersionLogToIcebergTransaction classifies each VersionLog into one of four strategies:'
    )
    
    # Commit classification diagram
    y = pdf.get_y() + 2
    bw3 = 38
    pdf.colored_box(70, y, 60, 14, 227, 116, 0, 'VersionLog.getActions()', font_size=6)
    pdf.arrow_down(100, y+14, 6)
    y += 24
    pdf.colored_box(10, y, bw3, 18, 52, 168, 83, 'AddFile Only\nAppendFiles', font_size=5.5)
    pdf.colored_box(55, y, bw3, 18, 234, 67, 53, 'RemoveFile Only\nDeleteFiles', font_size=5.5)
    pdf.colored_box(100, y, bw3, 18, 123, 31, 162, 'Add + Remove\nOverwriteFiles', font_size=5.5)
    pdf.colored_box(145, y, bw3, 18, 95, 99, 104, 'No Change\nDummy Append', font_size=5.5)
    y += 24
    pdf.colored_box(20, y, 155, 12, 21, 101, 192, 'tagCurrentSnapshot() -> createTag(delta-version-N) + createTag(delta-ts-T)', font_size=5.5)
    pdf.set_xy(20, y+18)
    pdf.set_font('Helvetica', 'I', 9)
    pdf.set_text_color(95, 99, 104)
    pdf.cell(0, 5, 'Figure 4: Commit Classification', align='C', new_x="LMARGIN", new_y="NEXT")
    pdf.ln(3)
    
    pdf.section_title('3.4 Provider / Factory Pattern')
    pdf.body_text(
        'DeltaLakeToIcebergMigrationActionsProvider serves as both provider interface and factory. '
        'It defines a default method snapshotDeltaLakeTable() that instantiates BaseSnapshotDeltaLakeTableAction. '
        'The inner class DefaultDeltaLakeToIcebergMigrationActions implements the Singleton pattern. '
        'Query engines can override this provider to supply custom implementations.'
    )
    
    pdf.section_title('3.5 Transaction Pattern')
    pdf.body_text(
        'The entire migration is wrapped in a single Iceberg Transaction created via '
        'icebergCatalog.newCreateTableTransaction(). All operations (append, delete, overwrite, property update, tag) '
        'are committed within this transaction. Only when commitTransaction() succeeds does the new Iceberg table become visible.'
    )
    
    pdf.section_title('3.6 Immutable Value Pattern')
    pdf.body_text(
        'The SnapshotDeltaLakeTable.Result interface is annotated with @Value.Immutable (Immutables library), '
        'generating ImmutableSnapshotDeltaLakeTable.Result at compile time. '
        'This pattern is consistent with Iceberg\'s project-wide convention.'
    )
    
    # ======================== CH4: CORE CLASSES ========================
    pdf.add_page()
    pdf.chapter_title('4. Core Class Design Details')
    
    pdf.section_title('4.1 SnapshotDeltaLakeTable Interface')
    pdf.body_text('Public API entry point extending Action<SnapshotDeltaLakeTable, Result>.')
    
    api_headers = ['Method', 'Return', 'Purpose']
    api_widths = [55, 15, 100]
    pdf.table_row(api_headers, api_widths, header=True)
    api_rows = [
        ['tableProperties(Map)', 'this', 'Batch set Iceberg table properties'],
        ['tableProperty(name, val)', 'this', 'Set a single table property'],
        ['tableLocation(location)', 'this', 'Override new table location (default: Delta location)'],
        ['as(TableIdentifier)', 'this', 'Set new Iceberg table identifier [Required]'],
        ['icebergCatalog(Catalog)', 'this', 'Set target Iceberg catalog [Required]'],
        ['deltaLakeConfiguration()', 'this', 'Set Hadoop conf for Delta access [Required]'],
        ['execute()', 'Result', 'Execute migration, return result summary'],
    ]
    for row in api_rows:
        pdf.table_row(row, api_widths)
    pdf.ln(5)
    
    pdf.section_title('4.2 BaseSnapshotDeltaLakeTableAction')
    pdf.body_text(
        'The most critical class in the module (~460 lines, package-private). Key internal fields:'
    )
    pdf.bullet('deltaLog (DeltaLog): Delta Lake transaction log, initialized via DeltaLog.forTable()')
    pdf.bullet('icebergCatalog (Catalog): Target Iceberg catalog for creating the new table')
    pdf.bullet('deltaLakeFileIO (HadoopFileIO): File I/O for reading data files and collecting metrics')
    pdf.bullet('deltaStartVersion (long): Earliest available version (may not be 0 after VACUUM)')
    pdf.bullet('additionalPropertiesBuilder (ImmutableMap.Builder): Accumulates user-specified properties')
    pdf.body_text(
        'Key Design Decision - Fault Tolerant Initial Version: The method commitInitialDeltaSnapshotToIcebergTransaction '
        'handles VACUUM-cleaned tables by iterating from deltaStartVersion upward until finding a constructable snapshot. '
        'Catches NotFoundException and DeltaStandaloneException to skip inaccessible versions.'
    )
    
    pdf.section_title('4.3 DeltaLakeDataTypeVisitor and DeltaLakeTypeToType')
    pdf.body_text(
        'DeltaLakeDataTypeVisitor<T>: Abstract class with static visit() dispatch. Recursively traverses '
        'Delta type tree (struct -> field -> atomic/array/map). Five abstract methods: struct(), field(), array(), map(), atomic().'
    )
    pdf.body_text(
        'DeltaLakeTypeToType extends visitor (T=Iceberg Type). Manages nextId counter for field IDs. '
        'Root fields use ordinal-based IDs; nested fields use auto-incrementing IDs. '
        'Correctly handles nullable vs. required semantics and preserves comments from Delta metadata.'
    )
    
    pdf.section_title('4.4 DeltaLakeToIcebergMigrationActionsProvider')
    pdf.body_text(
        'Combines Provider + Factory + Singleton patterns. Defines default method snapshotDeltaLakeTable() '
        'returning new BaseSnapshotDeltaLakeTableAction(). Inner class DefaultDeltaLakeToIcebergMigrationActions '
        'is a private singleton. Static method defaultActions() returns this singleton. '
        'Engines can override the provider with custom implementations.'
    )
    
    # ======================== CH5: CALL CHAINS ========================
    pdf.add_page()
    pdf.chapter_title('5. Key Scenario Call Chains')
    
    pdf.section_title('5.1 Complete Snapshot Migration (Primary Scenario)')
    pdf.code_block(
        'Client -> MigrationActionsProvider.defaultActions()\n'
        '  -> new BaseSnapshotDeltaLakeTableAction(location)\n'
        '  -> .as(identifier) .icebergCatalog(catalog) .deltaLakeConfiguration(conf)\n'
        '    -> DeltaLog.forTable(conf, location)  // init deltaLog\n'
        '    -> new HadoopFileIO(conf)  // init file IO\n'
        '    -> deltaLog.getVersionAtOrAfterTimestamp(0)  // find start version\n'
        '  -> .execute()\n'
        '    -> Preconditions.checkArgument(...)  // validate all params\n'
        '    -> deltaLog.update()  // get latest snapshot\n'
        '    -> convertDeltaLakeSchema(deltaSchema)\n'
        '      -> DeltaLakeDataTypeVisitor.visit(schema, new DeltaLakeTypeToType(schema))\n'
        '    -> getPartitionSpecFromDeltaSnapshot(schema, snapshot)\n'
        '    -> icebergCatalog.newCreateTableTransaction(...)\n'
        '    -> transaction.table().updateProperties().set(NameMapping).commit()\n'
        '    -> commitInitialDeltaSnapshotToIcebergTransaction(version, tx)\n'
        '    -> [loop] commitDeltaVersionLogToIcebergTransaction(vlog, tx)\n'
        '    -> icebergTransaction.commitTransaction()\n'
        '    -> return ImmutableResult{snapshotDataFilesCount}'
    )
    
    pdf.section_title('5.2 Initial Version Commit (Fault Tolerance)')
    pdf.code_block(
        'commitInitialDeltaSnapshotToIcebergTransaction(latestVersion, tx)\n'
        '  -> constructableStartVersion = deltaStartVersion\n'
        '  -> [while constructableStartVersion <= latestVersion]\n'
        '    -> deltaLog.getSnapshotForVersionAsOf(version).getAllFiles()\n'
        '    -> [for each AddFile]\n'
        '      -> buildDataFileFromAction(addFile, table)\n'
        '        -> getFullFilePath(path, deltaLog.getPath())\n'
        '        -> deltaLakeFileIO.newInputFile(fullPath)\n'
        '        -> file.exists() ?  // validate file presence\n'
        '        -> ParquetUtil.fileMetrics(file, metricsConfig, nameMapping)\n'
        '        -> DataFiles.builder(spec).withPath().withMetrics().build()\n'
        '    -> transaction.newAppend().appendFile(each).commit()\n'
        '    -> tagCurrentSnapshot(version, tx)\n'
        '      -> manageSnapshots().createTag("delta-version-N")\n'
        '      -> manageSnapshots().createTag("delta-ts-T")\n'
        '    -> return version  // success\n'
        '  -> [catch NotFoundException | DeltaStandaloneException]\n'
        '    -> constructableStartVersion++  // try next version'
    )
    
    pdf.section_title('5.3 VersionLog Incremental Commit')
    pdf.code_block(
        'commitDeltaVersionLogToIcebergTransaction(versionLog, tx)\n'
        '  -> versionLog.getActions().stream()\n'
        '    -> filter(action instanceof AddFile || RemoveFile)\n'
        '  -> [for each action] buildDataFileFromAction(action, table)\n'
        '    -> classify into filesToAdd / filesToRemove\n'
        '  -> [decision branch]\n'
        '    -> !filesToAdd.empty AND !filesToRemove.empty\n'
        '      -> tx.newOverwrite().addFile(each).deleteFile(each).commit()\n'
        '    -> !filesToAdd.empty\n'
        '      -> tx.newAppend().appendFile(each).commit()\n'
        '    -> !filesToRemove.empty\n'
        '      -> tx.newDelete().deleteFile(each).commit()\n'
        '    -> else\n'
        '      -> tx.newAppend().commit()  // dummy append\n'
        '  -> tagCurrentSnapshot(versionLog.getVersion(), tx)'
    )
    
    pdf.add_page()
    pdf.section_title('5.4 Type System Conversion')
    pdf.code_block(
        'DeltaLakeDataTypeVisitor.visit(deltaStructType, visitor)\n'
        '  -> [type is StructType]\n'
        '    -> for each StructField:\n'
        '      -> visit(field.getDataType(), visitor)  // RECURSIVE\n'
        '        -> [atomic] visitor.atomic(type)\n'
        '          -> DeltaLakeTypeToType.atomic(): map to Iceberg type\n'
        '        -> [array] visit(elementType) -> visitor.array(type, elem)\n'
        '          -> Types.ListType.ofOptional/ofRequired(nextId, elementType)\n'
        '        -> [map] visit(keyType), visit(valueType) -> visitor.map()\n'
        '          -> Types.MapType.ofOptional/ofRequired(nextId, nextId, k, v)\n'
        '        -> [struct] RECURSIVE into nested struct\n'
        '      -> visitor.field(field, typeResult)\n'
        '    -> visitor.struct(structType, fieldResults)\n'
        '      -> assign field IDs (ordinal for root, auto-increment for nested)\n'
        '      -> preserve nullable/required semantics\n'
        '      -> extract comment from field metadata\n'
        '      -> return Types.StructType.of(newFields)'
    )
    
    pdf.section_title('5.5 Data File Construction')
    pdf.code_block(
        'buildDataFileFromAction(action, table)\n'
        '  -> [instanceof AddFile]\n'
        '    -> extract path, size, partitionValues from AddFile\n'
        '  -> [instanceof RemoveFile]\n'
        '    -> extract path, size (Optional), partitionValues from RemoveFile\n'
        '  -> getFullFilePath(path, deltaLog.getPath())\n'
        '    -> URI.create(path) -> decode -> absolute? return : prepend tableRoot\n'
        '  -> Preconditions.checkArgument(partitionValues != null)\n'
        '  -> determineFileFormatFromPath(path)  // must be .parquet\n'
        '  -> deltaLakeFileIO.newInputFile(fullPath)\n'
        '  -> file.exists() ? : throw NotFoundException\n'
        '  -> fileSize = nullableFileSize ?? file.getLength()\n'
        '  -> MetricsConfig.forTable(table)\n'
        '  -> NameMappingParser.fromJson(nameMapping)\n'
        '  -> ParquetUtil.fileMetrics(file, metricsConfig, nameMapping)\n'
        '  -> DataFiles.builder(spec)\n'
        '    .withPath(fullPath).withFormat(PARQUET)\n'
        '    .withFileSizeInBytes(fileSize).withMetrics(metrics)\n'
        '    .withPartitionValues(partitionValueList).build()'
    )
    
    pdf.section_title('5.6 Spark Integration Scenario')
    pdf.code_block(
        'DeltaLakeToIcebergMigrationSparkIntegration.snapshotDeltaLakeTable(spark, id, loc)\n'
        '  -> Preconditions.checkArgument(spark, id, loc != null)\n'
        '  -> spark.sessionState().catalogManager().currentCatalog()\n'
        '  -> Spark3Util.catalogAndIdentifier(ctx, spark, id, defaultCatalog)\n'
        '  -> DeltaLakeToIcebergMigrationActionsProvider.defaultActions()\n'
        '    -> .snapshotDeltaLakeTable(deltaTableLocation)\n'
        '      -> new BaseSnapshotDeltaLakeTableAction(location)\n'
        '    -> .as(TableIdentifier.parse(catalogAndIdent.identifier()))\n'
        '    -> .deltaLakeConfiguration(spark.sessionState().newHadoopConf())\n'
        '    -> .icebergCatalog(Spark3Util.loadIcebergCatalog(spark, catalogName))\n'
        '  -> return SnapshotDeltaLakeTable  // ready for .execute()'
    )
    
    # ======================== CH6: SUMMARY ========================
    pdf.add_page()
    pdf.chapter_title('6. Summary and Design Merits')
    pdf.body_text(
        'The iceberg-delta-lake module is a masterclass in focused, well-designed migration tooling. '
        'Key architectural merits:'
    )
    pdf.bullet('Minimal Footprint, Maximum Impact: With only 5 main source files and ~600 lines of core logic, '
               'the module achieves complete, version-faithful Delta-to-Iceberg migration.')
    pdf.bullet('Zero-Copy Data Philosophy: No data files are copied or transformed. Only Iceberg metadata '
               'is created pointing to existing Parquet files, making migration instantaneous regardless of data volume.')
    pdf.bullet('Robust Fault Tolerance: The initial version search mechanism gracefully handles VACUUM-cleaned '
               'and log-cleaned Delta tables, automatically finding the first constructable version.')
    pdf.bullet('Full History Preservation: Every Delta version is replayed as a distinct Iceberg snapshot, '
               'with version and timestamp tags enabling time-travel queries on the migrated table.')
    pdf.bullet('Transactional Atomicity: The entire migration is wrapped in a single Iceberg transaction. '
               'If any step fails, no partial table is left behind.')
    pdf.bullet('Clean Separation of Concerns: Type conversion (Visitor), action creation (Provider/Factory), '
               'commit strategy (Strategy), and configuration (Builder) each have dedicated, single-responsibility classes.')
    pdf.bullet('Extensibility: The Provider pattern allows engine overrides. The Visitor pattern enables easy type additions. '
               'The commit classification can be extended with new Action type handlers.')
    pdf.bullet('Consistency with Iceberg Conventions: Package-private implementations, Immutables for value objects, '
               'Preconditions for validation, Action<ThisT, R> interface pattern, and NameMapping for schema evolution.')
    pdf.ln(5)
    pdf.body_text(
        'Overall, this module demonstrates that well-chosen design patterns and a clear architectural vision '
        'can produce a highly functional migration tool with minimal code complexity, while maintaining the high '
        'quality standards expected of the Apache Iceberg project.'
    )
    
    # Save
    pdf.output(out)
    print(f"PDF generated successfully: {out}")

out = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'Iceberg_Delta_Lake_Module_Design_Document.pdf')
build_pdf()
