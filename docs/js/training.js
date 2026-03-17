/* =============================================
   training.js — 教育訓練教材互動邏輯
   大豐環保｜法務及環安課
   ============================================= */

(function () {
  'use strict';

  /* ===== 進度條更新 ===== */
  var progressFill = document.querySelector('.progress-bar-fill');
  var navProgress = document.querySelector('.nav-progress');

  function updateProgress() {
    var scrollTop = window.scrollY;
    var docHeight = document.documentElement.scrollHeight - window.innerHeight;
    var pct = docHeight > 0 ? Math.round((scrollTop / docHeight) * 100) : 0;
    if (pct > 100) pct = 100;
    if (progressFill) progressFill.style.width = pct + '%';
    if (navProgress) navProgress.textContent = pct + '%';
  }

  window.addEventListener('scroll', updateProgress);
  updateProgress();

  /* ===== 章節導航按鈕高亮 ===== */
  var chapterBtns = document.querySelectorAll('.chapter-nav-btn');
  var chapterSections = [];

  chapterBtns.forEach(function (btn) {
    var targetId = btn.getAttribute('data-target');
    if (targetId) {
      var el = document.getElementById(targetId);
      if (el) chapterSections.push({ btn: btn, el: el });
    }
    btn.addEventListener('click', function () {
      var target = document.getElementById(this.getAttribute('data-target'));
      if (target) {
        target.scrollIntoView({ behavior: 'smooth', block: 'start' });
      }
    });
  });

  function updateActiveChapter() {
    var scrollPos = window.scrollY + 120;
    var activeIdx = 0;
    for (var i = 0; i < chapterSections.length; i++) {
      if (chapterSections[i].el.offsetTop <= scrollPos) {
        activeIdx = i;
      }
    }
    chapterBtns.forEach(function (btn) { btn.classList.remove('active'); });
    if (chapterBtns[activeIdx]) chapterBtns[activeIdx].classList.add('active');
  }

  window.addEventListener('scroll', updateActiveChapter);
  updateActiveChapter();

  /* ===== 測驗邏輯 ===== */
  // 每個測驗區塊的結構：
  // .quiz-section[data-quiz-id]
  //   .quiz-question[data-answer="A"]
  //     .quiz-option[data-value="A"]
  //   .quiz-submit-btn
  //   .quiz-result

  document.querySelectorAll('.quiz-section').forEach(function (quiz) {
    var questions = quiz.querySelectorAll('.quiz-question');
    var submitBtn = quiz.querySelector('.quiz-submit-btn');
    var resultDiv = quiz.querySelector('.quiz-result');
    var answered = {};

    // 選項點擊
    questions.forEach(function (q, qIdx) {
      var options = q.querySelectorAll('.quiz-option');
      options.forEach(function (opt) {
        opt.addEventListener('click', function () {
          // 如果已提交，不再允許改選
          if (quiz.classList.contains('submitted')) return;
          // 取消同題其他選項
          options.forEach(function (o) { o.classList.remove('selected'); });
          opt.classList.add('selected');
          answered[qIdx] = opt.getAttribute('data-value');
        });
      });
    });

    // 提交
    if (submitBtn) {
      submitBtn.addEventListener('click', function () {
        if (quiz.classList.contains('submitted')) return;
        // 檢查是否所有題目都已作答
        var allAnswered = true;
        questions.forEach(function (q, i) {
          if (!answered[i]) allAnswered = false;
        });
        if (!allAnswered) {
          alert('請回答所有題目後再提交！');
          return;
        }

        quiz.classList.add('submitted');
        submitBtn.disabled = true;
        submitBtn.textContent = '已提交';

        var correct = 0;
        var total = questions.length;

        questions.forEach(function (q, i) {
          var correctAnswer = q.getAttribute('data-answer');
          var options = q.querySelectorAll('.quiz-option');
          var feedback = q.querySelector('.quiz-feedback');

          options.forEach(function (opt) {
            var val = opt.getAttribute('data-value');
            if (val === correctAnswer) {
              opt.classList.add('correct');
            }
            if (val === answered[i] && val !== correctAnswer) {
              opt.classList.add('wrong');
            }
          });

          if (answered[i] === correctAnswer) {
            correct++;
            if (feedback) {
              feedback.classList.add('show', 'correct-fb');
            }
          } else {
            if (feedback) {
              feedback.classList.add('show', 'wrong-fb');
            }
          }
        });

        // 顯示結果
        if (resultDiv) {
          resultDiv.classList.add('show');
          var pct = Math.round((correct / total) * 100);
          if (pct >= 80) {
            resultDiv.classList.add('pass');
            resultDiv.innerHTML = '得分：' + correct + '/' + total + '（' + pct + '%）<br>恭喜通過！請繼續下一課';
          } else {
            resultDiv.classList.add('fail');
            resultDiv.innerHTML = '得分：' + correct + '/' + total + '（' + pct + '%）<br>未達 80 分，請複習後重新作答';
          }
        }
      });
    }
  });

  /* ===== 底部導航按鈕 ===== */
  var prevBtn = document.getElementById('prevChapter');
  var nextBtn = document.getElementById('nextChapter');

  if (prevBtn) {
    prevBtn.addEventListener('click', function () {
      var currentIdx = getCurrentChapterIdx();
      if (currentIdx > 0) {
        chapterSections[currentIdx - 1].el.scrollIntoView({ behavior: 'smooth', block: 'start' });
      }
    });
  }

  if (nextBtn) {
    nextBtn.addEventListener('click', function () {
      var currentIdx = getCurrentChapterIdx();
      if (currentIdx < chapterSections.length - 1) {
        chapterSections[currentIdx + 1].el.scrollIntoView({ behavior: 'smooth', block: 'start' });
      }
    });
  }

  function getCurrentChapterIdx() {
    var scrollPos = window.scrollY + 120;
    var idx = 0;
    for (var i = 0; i < chapterSections.length; i++) {
      if (chapterSections[i].el.offsetTop <= scrollPos) idx = i;
    }
    return idx;
  }

})();
