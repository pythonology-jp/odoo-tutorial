odoo.define('estate.utils_tests', function (require) {
"use strict";

function add(a, b) {
    return a + b;
}

QUnit.module('estate', {}, function () {
    QUnit.module('test add', {}, function () {
        QUnit.test('add two numbers', assert => {
            assert.expect(2)
            assert.strictEqual(add(1, 1), 2);
            assert.strictEqual(add(1, 3), 4);
        });
    });
});
});