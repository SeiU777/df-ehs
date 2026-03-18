/* =============================================
   auth.js — 靜態網站密碼保護
   大豐環保｜法務及環安課
   ============================================= */

(function () {
  'use strict';

  /* 編碼後的密碼（XOR 編碼，非明文） */
  var _k = 42;
  var _d = [110,75,26,25,26,24,76,69,68,24,26,24,28,15];

  /* 驗證函式 */
  function _verify(input) {
    if (input.length !== _d.length) return false;
    for (var i = 0; i < _d.length; i++) {
      if ((input.charCodeAt(i) ^ _k) !== _d[i]) return false;
    }
    return true;
  }

  /* 檢查是否已登入（暫時停用密碼保護） */
  function isAuthenticated() {
    return true; /* 原始邏輯：sessionStorage.getItem('df-ehs-auth') === 'ok' */
  }

  /* 設定已登入 */
  function setAuthenticated() {
    sessionStorage.setItem('df-ehs-auth', 'ok');
  }

  /* 登出 */
  function logout() {
    sessionStorage.removeItem('df-ehs-auth');
  }

  /* 公開 API */
  window.dfAuth = {
    verify: _verify,
    isAuthenticated: isAuthenticated,
    setAuthenticated: setAuthenticated,
    logout: logout
  };
})();
