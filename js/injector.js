/* THE CODE BELOW SHOULD BE INJECTED TO THE JS FILE
   AT https://epsf.ticketmaster.com/eps-d 
   IN ORDER TO OBTAIN A REESE84 TOKEN FROM THE SERVER */

/**
 * Reference: https://epsf.ticketmaster.com/eps-d
 */
const reese84HashObj = {
  hash: function (_0x32cda0) {
    _0x32cda0 = unescape(encodeURIComponent(_0x32cda0));
    for (
      var _0x354dff = [0x5a827999, 0x6ed9eba1, 0x8f1bbcdc, 0xca62c1d6],
        _0x184815 =
          (_0x32cda0 += String['fromCharCode'](0x80))['length'] / 0x4 + 0x2,
        _0x4f0814 = Math['ceil'](_0x184815 / 0x10),
        _0xb67cd8 = new Array(_0x4f0814),
        _0x3db23f = 0x0;
      _0x3db23f < _0x4f0814;
      _0x3db23f++
    ) {
      _0xb67cd8[_0x3db23f] = new Array(0x10);
      for (var _0x4d1d12 = 0x0; _0x4d1d12 < 0x10; _0x4d1d12++)
        _0xb67cd8[_0x3db23f][_0x4d1d12] =
          (_0x32cda0['charCodeAt'](0x40 * _0x3db23f + 0x4 * _0x4d1d12) <<
            0x18) |
          (_0x32cda0['charCodeAt'](0x40 * _0x3db23f + 0x4 * _0x4d1d12 + 0x1) <<
            0x10) |
          (_0x32cda0['charCodeAt'](0x40 * _0x3db23f + 0x4 * _0x4d1d12 + 0x2) <<
            0x8) |
          _0x32cda0['charCodeAt'](0x40 * _0x3db23f + 0x4 * _0x4d1d12 + 0x3);
    }
    (_0xb67cd8[_0x4f0814 - 0x1][0xe] =
      (0x8 * (_0x32cda0['length'] - 0x1)) / Math['pow'](0x2, 0x20)),
      (_0xb67cd8[_0x4f0814 - 0x1][0xe] = Math['floor'](
        _0xb67cd8[_0x4f0814 - 0x1][0xe]
      )),
      (_0xb67cd8[_0x4f0814 - 0x1][0xf] =
        (0x8 * (_0x32cda0['length'] - 0x1)) & 0xffffffff);
    var _0x4964ee,
      _0x1f8408,
      _0x393864,
      _0x4e34f7,
      _0x2bdc40,
      _0x725508 = 0x67452301,
      _0x69fa2d = 0xefcdab89,
      _0xc2205d = 0x98badcfe,
      _0x4d6fc6 = 0x10325476,
      _0x531366 = 0xc3d2e1f0,
      _0xe1407f = new Array(0x50);
    for (_0x3db23f = 0x0; _0x3db23f < _0x4f0814; _0x3db23f++) {
      for (var _0x19ef55 = 0x0; _0x19ef55 < 0x10; _0x19ef55++)
        _0xe1407f[_0x19ef55] = _0xb67cd8[_0x3db23f][_0x19ef55];
      for (_0x19ef55 = 0x10; _0x19ef55 < 0x50; _0x19ef55++)
        _0xe1407f[_0x19ef55] = reese84HashObj['ROTL'](
          _0xe1407f[_0x19ef55 - 0x3] ^
            _0xe1407f[_0x19ef55 - 0x8] ^
            _0xe1407f[_0x19ef55 - 0xe] ^
            _0xe1407f[_0x19ef55 - 0x10],
          0x1
        );
      (_0x4964ee = _0x725508),
        (_0x1f8408 = _0x69fa2d),
        (_0x393864 = _0xc2205d),
        (_0x4e34f7 = _0x4d6fc6),
        (_0x2bdc40 = _0x531366);
      for (_0x19ef55 = 0x0; _0x19ef55 < 0x50; _0x19ef55++) {
        var _0x1f693f = Math['floor'](_0x19ef55 / 0x14),
          _0x1e561e =
            (reese84HashObj['ROTL'](_0x4964ee, 0x5) +
              reese84HashObj['f'](_0x1f693f, _0x1f8408, _0x393864, _0x4e34f7) +
              _0x2bdc40 +
              _0x354dff[_0x1f693f] +
              _0xe1407f[_0x19ef55]) &
            0xffffffff;
        (_0x2bdc40 = _0x4e34f7),
          (_0x4e34f7 = _0x393864),
          (_0x393864 = reese84HashObj['ROTL'](_0x1f8408, 0x1e)),
          (_0x1f8408 = _0x4964ee),
          (_0x4964ee = _0x1e561e);
      }
      (_0x725508 = (_0x725508 + _0x4964ee) & 0xffffffff),
        (_0x69fa2d = (_0x69fa2d + _0x1f8408) & 0xffffffff),
        (_0xc2205d = (_0xc2205d + _0x393864) & 0xffffffff),
        (_0x4d6fc6 = (_0x4d6fc6 + _0x4e34f7) & 0xffffffff),
        (_0x531366 = (_0x531366 + _0x2bdc40) & 0xffffffff);
    }
    return (
      reese84HashObj['toHexStr'](_0x725508) +
      reese84HashObj['toHexStr'](_0x69fa2d) +
      reese84HashObj['toHexStr'](_0xc2205d) +
      reese84HashObj['toHexStr'](_0x4d6fc6) +
      reese84HashObj['toHexStr'](_0x531366)
    );
  },
  f: function (_0x4a2ab7, _0x15ec48, _0x2f0b8e, _0x6ffd09) {
    switch (_0x4a2ab7) {
      case 0x0:
        return (_0x15ec48 & _0x2f0b8e) ^ (~_0x15ec48 & _0x6ffd09);
      case 0x1:
      case 0x3:
        return _0x15ec48 ^ _0x2f0b8e ^ _0x6ffd09;
      case 0x2:
        return (
          (_0x15ec48 & _0x2f0b8e) ^
          (_0x15ec48 & _0x6ffd09) ^
          (_0x2f0b8e & _0x6ffd09)
        );
    }
  },
  ROTL: function (_0x11e783, _0x3f2f62) {
    return (_0x11e783 << _0x3f2f62) | (_0x11e783 >>> (0x20 - _0x3f2f62));
  },
  toHexStr: function (_0x125300) {
    for (var _0x39e29d = '', _0xa51676 = 0x7; _0xa51676 >= 0x0; _0xa51676--)
      _0x39e29d += ((_0x125300 >>> (0x4 * _0xa51676)) & 0xf)['toString'](0x10);
    return _0x39e29d;
  },
};

/**
 * Reference: https://epsf.ticketmaster.com/eps-d
 */
function _0xbae375() {
  return Date['now'] ? Date['now']() : new Date()['getTime']();
}

/**
 * Reference: https://epsf.ticketmaster.com/eps-d
 */
const timerFactory = (function () {
  /**
    * 
    * start: ƒ (_0x3deed1)
      startInternal: ƒ (_0xd257e7)
      stop: ƒ (_0x975271)
      stopInternal: ƒ (_0x2f5e67)
      summary: ƒ ()
    */
  function _0x1efe8f() {
    (this['marks'] = {}), (this['measures'] = {});
  }
  return (
    (_0x1efe8f['prototype']['start'] = function (_0x3deed1) {
      this['marks'][_0x3deed1] = _0xbae375();
    }),
    (_0x1efe8f['prototype']['startInternal'] = function (_0xd257e7) {}),
    (_0x1efe8f['prototype']['stop'] = function (_0x975271) {
      this['measures'][_0x975271] = _0xbae375() - this['marks'][_0x975271];
    }),
    (_0x1efe8f['prototype']['stopInternal'] = function (_0x2f5e67) {}),
    (_0x1efe8f['prototype']['summary'] = function () {
      return this['measures'];
    }),
    _0x1efe8f
  );
})();

/* injector code starts here */

const getInterrogation = async () => {
  const INTERROGATOR = 'reese84interrogator',
    INTERROGATION = 'interrogate';
  const interrogationFn = window[INTERROGATOR];
  if (!interrogationFn) {
    throw new Error('Interrogation function not extracted');
  }
  let fn = {};
  const timer = new timerFactory();
  timer.start('total');

  interrogationFn.call(fn, reese84HashObj.hash, timer);
  const res = await new Promise(fn[INTERROGATION]);
  return [res, timer];
};

/**
 * main function
 */
(async function () {
  const [reese84, timer] = await getInterrogation();
  const body = {
    error: null,
    old_token: null,
    performance: { interrogation: timer.measures.interrogation },
    solution: { interrogation: reese84 },
  };
  console.log(body);
  return body;
})();
