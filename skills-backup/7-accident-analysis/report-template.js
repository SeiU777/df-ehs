// 職災案件分析報告 .docx 產生器
// 用法: node report-template.js <data.json> <output.docx>
// 或由 Skill 直接 require 後呼叫 generateReport(data, outputPath)

const path = require('path');
const fs = require('fs');

const homedir = require('os').homedir();
const modulePath = path.join(homedir, 'Documents/claude/職安/參考資料/安委會/pptx-workspace/node_modules/docx');
const {
  Document, Packer, Paragraph, TextRun, Table, TableRow, TableCell,
  Header, Footer, AlignmentType, HeadingLevel, BorderStyle, WidthType,
  ShadingType, VerticalAlign, PageNumber, LevelFormat, PageBreak
} = require(modulePath);

// ===== 樣式常數 =====
const C = {
  pri: "1B4F72", sec: "2E86C1", accent: "D4E6F1",
  hdr: "1B4F72", gray: "F2F3F4", white: "FFFFFF",
  black: "000000", red: "C0392B", orange: "E67E22", green: "27AE60",
};
const FONT = "Microsoft JhengHei";
const border = { style: BorderStyle.SINGLE, size: 1, color: "B0B0B0" };
const cb = { top: border, bottom: border, left: border, right: border };
const tb = { style: BorderStyle.SINGLE, size: 2, color: C.pri };
const thickB = { top: tb, bottom: tb, left: tb, right: tb };
const grayBg = { shading: { fill: C.gray, type: ShadingType.CLEAR } };

// ===== 輔助函式 =====
function hCell(text, w, opts = {}) {
  return new TableCell({
    borders: thickB, width: { size: w, type: WidthType.DXA },
    shading: { fill: C.hdr, type: ShadingType.CLEAR },
    verticalAlign: VerticalAlign.CENTER, ...opts,
    children: [new Paragraph({
      alignment: AlignmentType.CENTER, spacing: { before: 60, after: 60 },
      children: [new TextRun({ text, bold: true, color: C.white, size: 22, font: FONT })]
    })]
  });
}

function lCell(text, w) {
  return new TableCell({
    borders: cb, width: { size: w, type: WidthType.DXA },
    shading: { fill: C.accent, type: ShadingType.CLEAR },
    verticalAlign: VerticalAlign.CENTER,
    children: [new Paragraph({
      alignment: AlignmentType.CENTER, spacing: { before: 40, after: 40 },
      children: [new TextRun({ text, bold: true, size: 21, font: FONT, color: C.pri })]
    })]
  });
}

function dCell(text, w, opts = {}) {
  return new TableCell({
    borders: cb, width: { size: w, type: WidthType.DXA },
    verticalAlign: VerticalAlign.CENTER, ...opts,
    children: [new Paragraph({
      spacing: { before: 40, after: 40 }, indent: { left: 80 },
      children: [new TextRun({ text, size: 21, font: FONT })]
    })]
  });
}

function mCell(lines, w, opts = {}) {
  return new TableCell({
    borders: cb, width: { size: w, type: WidthType.DXA },
    verticalAlign: VerticalAlign.TOP, ...opts,
    children: lines.map(l => new Paragraph({
      spacing: { before: 30, after: 30 }, indent: { left: 120 },
      children: [new TextRun({ text: l, size: 21, font: FONT })]
    }))
  });
}

function colorLabelCell(text, w, color, rowSpan) {
  return new TableCell({
    borders: cb, width: { size: w, type: WidthType.DXA },
    shading: { fill: color, type: ShadingType.CLEAR },
    verticalAlign: VerticalAlign.CENTER,
    ...(rowSpan ? { rowSpan } : {}),
    children: [new Paragraph({
      alignment: AlignmentType.CENTER,
      children: [new TextRun({ text, bold: true, size: 21, font: FONT })]
    })]
  });
}

function levelCell(text, w, color) {
  return new TableCell({
    borders: cb, width: { size: w, type: WidthType.DXA },
    verticalAlign: VerticalAlign.CENTER,
    children: [new Paragraph({
      alignment: AlignmentType.CENTER, spacing: { before: 40, after: 40 },
      children: [new TextRun({ text, size: 21, font: FONT, bold: true, color })]
    })]
  });
}

function para(text, opts = {}) {
  return new Paragraph({
    spacing: { before: 80, after: 80 }, indent: { left: 240 }, ...opts,
    children: [new TextRun({ text, size: 22, font: FONT })]
  });
}

function heading1(text) {
  return new Paragraph({
    heading: HeadingLevel.HEADING_1,
    children: [new TextRun({ text, bold: true })]
  });
}

function heading2(text) {
  return new Paragraph({
    heading: HeadingLevel.HEADING_2,
    children: [new TextRun({ text, bold: true })]
  });
}

function subHeading(text) {
  return new Paragraph({
    spacing: { before: 120, after: 60 }, indent: { left: 240 },
    children: [new TextRun({ text, bold: true, size: 23, color: C.sec, font: FONT })]
  });
}

// ===== 主要報告產生函式 =====
function generateReport(d, outputPath) {
  const doc = new Document({
    styles: {
      default: { document: { run: { font: FONT, size: 22 } } },
      paragraphStyles: [
        { id: "Title", name: "Title", basedOn: "Normal",
          run: { size: 44, bold: true, color: C.pri, font: FONT },
          paragraph: { spacing: { before: 120, after: 60 }, alignment: AlignmentType.CENTER } },
        { id: "Heading1", name: "Heading 1", basedOn: "Normal", next: "Normal", quickFormat: true,
          run: { size: 30, bold: true, color: C.pri, font: FONT },
          paragraph: { spacing: { before: 300, after: 120 }, outlineLevel: 0 } },
        { id: "Heading2", name: "Heading 2", basedOn: "Normal", next: "Normal", quickFormat: true,
          run: { size: 26, bold: true, color: C.sec, font: FONT },
          paragraph: { spacing: { before: 200, after: 100 }, outlineLevel: 1 } }
      ]
    },
    sections: [{
      properties: {
        page: {
          margin: { top: 1200, right: 1200, bottom: 1200, left: 1200 },
          size: { width: 11906, height: 16838 }
        }
      },
      headers: { default: new Header({ children: [new Paragraph({
        alignment: AlignmentType.RIGHT,
        children: [new TextRun({ text: "大豐環保股份有限公司  |  職災案件分析報告", size: 16, color: "888888", font: FONT })]
      })] }) },
      footers: { default: new Footer({ children: [new Paragraph({
        alignment: AlignmentType.CENTER,
        children: [
          new TextRun({ text: "第 ", size: 16, color: "888888", font: FONT }),
          new TextRun({ children: [PageNumber.CURRENT], size: 16, color: "888888" }),
          new TextRun({ text: " 頁", size: 16, color: "888888", font: FONT })
        ]
      })] }) },
      children: [
        // ==========================================
        // 封面標題
        // ==========================================
        new Paragraph({ spacing: { before: 200 }, children: [] }),
        new Paragraph({ heading: HeadingLevel.TITLE,
          children: [new TextRun({ text: "職災案件分析報告", bold: true, size: 44, color: C.pri, font: FONT })] }),
        new Paragraph({ alignment: AlignmentType.CENTER, spacing: { after: 60 },
          children: [new TextRun({ text: "工安單位災害原因調查分析", size: 28, color: C.sec, font: FONT })] }),
        new Paragraph({ alignment: AlignmentType.CENTER, spacing: { after: 300 },
          children: [new TextRun({ text: `案件：${d.info.date} ${d.info.name}（${d.info.nationality || ''}）${d.info.summary}`, size: 22, color: "666666", font: FONT })] }),

        // ==========================================
        // Part A：公司內部要求欄位
        // ==========================================
        new Paragraph({ alignment: AlignmentType.CENTER, spacing: { before: 100, after: 200 },
          children: [new TextRun({ text: "Part A：公司內部要求欄位", bold: true, size: 28, color: C.pri, font: FONT })] }),

        // 一、案件基本資訊
        heading1("一、案件基本資訊"),
        new Table({ columnWidths: [2200, 3200, 2200, 1900], rows: [
          new TableRow({ children: [hCell("項目", 2200), hCell("內容", 3200), hCell("項目", 2200), hCell("內容", 1900)] }),
          ...d.info.rows.map(r => new TableRow({ children: [
            lCell(r[0], 2200), dCell(r[1], 3200), lCell(r[2], 2200), dCell(r[3], 1900)
          ] }))
        ] }),

        // 二、事故經過
        heading1("二、事故經過（發生單位描述）"),
        para(d.description),

        // 三、改善對策（發生單位提出）
        heading1("三、改善對策（發生單位提出）"),
        para(d.unitImprovement),

        // 四、災害原因分析（下拉選項 + 文字說明）
        heading1("四、災害原因分析（工安單位）"),

        subHeading("4.1 不安全行為（災害原因分析）"),
        para(`選項：${d.partA.unsafeBehavior.selected}`),
        para(`說明：${d.partA.unsafeBehavior.description}`),

        subHeading("4.2 不安全狀況"),
        para(`選項：${d.partA.unsafeCondition.selected}`),
        para(`說明：${d.partA.unsafeCondition.description}`),

        subHeading("4.3 基本原因"),
        para(`選項：${d.partA.rootCause.selected}`),
        para(`說明：${d.partA.rootCause.description}`),

        // 五、預防再發措施
        heading1("五、預防再發措施"),
        ...d.partA.prevention.map(line => para(line)),

        // 六、本案責任初步判定
        heading1("六、本案責任初步判定"),
        ...d.partA.responsibility.map(line => para(line)),

        // ==========================================
        // Part B：進階分析
        // ==========================================
        new Paragraph({ children: [new PageBreak()] }),
        new Paragraph({ alignment: AlignmentType.CENTER, spacing: { before: 100, after: 200 },
          children: [new TextRun({ text: "Part B：進階分析（工安單位延伸）", bold: true, size: 28, color: C.pri, font: FONT })] }),

        // 七、直接原因分析
        heading1("七、直接原因分析"),
        new Table({ columnWidths: [2400, 7100], rows: [
          new TableRow({ children: [hCell("分析項目", 2400), hCell("分析內容", 7100)] }),
          new TableRow({ children: [lCell("災害類型", 2400), dCell(d.partB.directCause.type, 7100)] }),
          new TableRow({ children: [lCell("媒介物", 2400), dCell(d.partB.directCause.medium, 7100)] }),
          new TableRow({ children: [lCell("接觸方式", 2400), mCell(d.partB.directCause.contact, 7100)] }),
        ] }),

        // 八、間接原因深度分析
        heading1("八、間接原因深度分析"),

        heading2("8.1 不安全行為分析"),
        para("依公司電子表單選項進行主因/次因/輔因判定："),
        new Table({ columnWidths: [600, 3400, 1200, 4300], rows: [
          new TableRow({ children: [hCell("項次", 600), hCell("不安全行為選項", 3400), hCell("關聯程度", 1200), hCell("分析說明", 4300)] }),
          ...d.partB.unsafeBehaviorAnalysis.map((item, i) => new TableRow({ children: [
            dCell(item.id, 600, i % 2 ? {} : grayBg),
            dCell(item.name, 3400, i % 2 ? {} : grayBg),
            levelCell(item.level, 1200, item.level === "★ 主因" ? C.red : item.level === "次因" ? C.orange : C.sec),
            dCell(item.desc, 4300, i % 2 ? {} : grayBg),
          ] }))
        ] }),

        heading2("8.2 不安全狀況分析"),
        para("依公司電子表單選項進行主因/次因/輔因判定："),
        new Table({ columnWidths: [600, 3400, 1200, 4300], rows: [
          new TableRow({ children: [hCell("項次", 600), hCell("不安全狀況選項", 3400), hCell("關聯程度", 1200), hCell("分析說明", 4300)] }),
          ...d.partB.unsafeConditionAnalysis.map((item, i) => new TableRow({ children: [
            dCell(item.id, 600, i % 2 ? {} : grayBg),
            dCell(item.name, 3400, i % 2 ? {} : grayBg),
            levelCell(item.level, 1200, item.level === "★ 主因" ? C.red : item.level === "次因" ? C.orange : C.sec),
            dCell(item.desc, 4300, i % 2 ? {} : grayBg),
          ] }))
        ] }),

        // 九、基本原因深度分析
        heading1("九、基本原因深度分析"),
        para("依公司電子表單選項進行主因/次因/輔因判定："),
        new Table({ columnWidths: [600, 3400, 1200, 4300], rows: [
          new TableRow({ children: [hCell("項次", 600), hCell("基本原因選項", 3400), hCell("關聯程度", 1200), hCell("分析說明", 4300)] }),
          ...d.partB.rootCauseAnalysis.map((item, i) => new TableRow({ children: [
            dCell(item.id, 600, i % 2 ? {} : grayBg),
            dCell(item.name, 3400, i % 2 ? {} : grayBg),
            levelCell(item.level, 1200, item.level === "★ 主因" ? C.red : item.level === "次因" ? C.orange : C.sec),
            dCell(item.desc, 4300, i % 2 ? {} : grayBg),
          ] }))
        ] }),

        // 十、人為失效模式分析
        heading1("十、人為失效模式分析（依 HSG48 架構）"),
        para("依據英國健康安全署 HSG48《減少錯誤與影響行為》之人為失誤分類架構分析："),
        new Table({ columnWidths: [2200, 2600, 4700], rows: [
          new TableRow({ children: [hCell("失誤類型", 2200), hCell("分類", 2600), hCell("本案對應分析", 4700)] }),
          ...d.partB.hsg48.map(item => new TableRow({ children: [
            dCell(item.type, 2200, { shading: { fill: item.bg || C.gray, type: ShadingType.CLEAR } }),
            dCell(item.category, 2600),
            dCell(item.analysis, 4700),
          ] }))
        ] }),

        // 十一、因果分析鏈
        heading1("十一、因果分析鏈（Why Tree）"),
        new Table({ columnWidths: [800, 3600, 5100], rows: [
          new TableRow({ children: [hCell("層級", 800), hCell("問題", 3600), hCell("回答", 5100)] }),
          ...d.partB.whyTree.map((item, i) => new TableRow({ children: [
            dCell(item.level, 800, i % 2 ? {} : grayBg),
            dCell(item.question, 3600, i % 2 ? {} : grayBg),
            dCell(item.answer, 5100, i % 2 ? {} : grayBg),
          ] }))
        ] }),

        // 十二、改善對策建議
        heading1("十二、改善對策建議（風險控制層級）"),
        new Table({ columnWidths: [600, 1600, 3400, 2400, 1500], rows: [
          new TableRow({ children: [hCell("項次", 600), hCell("控制層級", 1600), hCell("改善措施", 3400), hCell("執行說明", 2400), hCell("建議期限", 1500)] }),
          ...d.partB.improvements.map((item, i) => new TableRow({ children: [
            dCell(String(i + 1), 600, i % 2 ? {} : grayBg),
            dCell(item.level, 1600, i % 2 ? {} : grayBg),
            dCell(item.measure, 3400, i % 2 ? {} : grayBg),
            dCell(item.detail, 2400, i % 2 ? {} : grayBg),
            dCell(item.deadline, 1500, i % 2 ? {} : grayBg),
          ] }))
        ] }),

        // 十三、發生單位改善對策評析
        heading1("十三、發生單位改善對策評析"),
        new Table({ columnWidths: [2400, 7100], rows: [
          new TableRow({ children: [hCell("評析面向", 2400), hCell("工安單位意見", 7100)] }),
          ...d.partB.unitImprovementReview.map((item, i) => new TableRow({ children: [
            lCell(item.aspect, 2400),
            mCell(item.content, 7100, i % 2 ? grayBg : {}),
          ] }))
        ] }),

        // 十四、間接原因管理檢討
        heading1("十四、間接原因管理檢討"),
        new Table({ columnWidths: [2400, 7100], rows: [
          new TableRow({ children: [hCell("管理面向", 2400), hCell("檢討內容與建議", 7100)] }),
          ...d.partB.managementReview.map((item, i) => new TableRow({ children: [
            lCell(item.aspect, 2400),
            mCell(item.content, 7100, i % 2 ? grayBg : {}),
          ] }))
        ] }),

        // 十五、結論
        heading1("十五、結論"),
        ...d.conclusion.map(line => para(line)),

        // 簽核欄
        new Paragraph({ spacing: { before: 400 }, children: [] }),
        new Table({ columnWidths: [3170, 3170, 3170], rows: [
          new TableRow({ children: [hCell("製表", 3170), hCell("審核", 3170), hCell("核准", 3170)] }),
          new TableRow({ height: { value: 1200, rule: "atLeast" }, children: [
            dCell("工安單位", 3170), dCell("", 3170), dCell("", 3170)
          ] }),
          new TableRow({ children: [
            lCell("日期：    年    月    日", 3170),
            lCell("日期：    年    月    日", 3170),
            lCell("日期：    年    月    日", 3170),
          ] }),
        ] }),
        new Paragraph({ spacing: { before: 200 }, children: [] }),
      ]
    }]
  });

  return Packer.toBuffer(doc).then(buffer => {
    fs.writeFileSync(outputPath, buffer);
    console.log(`報告已生成: ${outputPath}`);
    return outputPath;
  });
}

// CLI 模式
if (require.main === module) {
  const [,, dataFile, outputFile] = process.argv;
  if (!dataFile || !outputFile) {
    console.log('用法: node report-template.js <data.json> <output.docx>');
    process.exit(1);
  }
  const data = JSON.parse(fs.readFileSync(dataFile, 'utf8'));
  generateReport(data, outputFile).catch(console.error);
}

module.exports = { generateReport };
