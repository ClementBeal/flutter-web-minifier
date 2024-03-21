# Constants and enums

# Constant value

Let's take this enum (I suppose it's an enum) from a build :

```js
B.nA = new A.b(8589935146);
B.nB = new A.b(8589935147);
B.A0 = new A.b(8589935148);
B.nC = new A.b(8589935149);
B.f2 = new A.b(8589935150);
B.nD = new A.b(8589935151);
B.f3 = new A.b(8589935152);
B.f4 = new A.b(8589935153);
B.f5 = new A.b(8589935154);
B.f6 = new A.b(8589935155);
B.f7 = new A.b(8589935156);
B.f8 = new A.b(8589935157);
B.f9 = new A.b(8589935158);
```

We can notice than the values just an incrementation. We could extract the first value into a new variable and apply the operator `++` or `+1`;

```js
var x = 8589935146;
B.nA = new A.b(x);
B.nB = new A.b(x + 1);
B.A0 = new A.b(x + 2);
B.nC = new A.b(x + 3);
B.f2 = new A.b(x + 4);
B.nD = new A.b(x + 5);
B.f3 = new A.b(x + 6);
B.f4 = new A.b(x + 7);
B.f5 = new A.b(x + 8);
B.f6 = new A.b(x + 9);
B.f7 = new A.b(x + 10);
B.f8 = new A.b(x + 11);
B.f9 = new A.b(x + 12);
```

## Enum `autofill`

In flutter, there is an enum used to provide autofill to the text fields.
All the values of the enum are copied to the final JS file like this short code :

```js
"tel-local-suffix",
  "telephoneNumberNational",
  "tel-national",
  "transactionAmount",
  "transaction-amount",
  "transactionCurrency",
  "transaction-currency";
```

The complete line is about **1700 bytes**. We should be able to keep the values that we need

## HCL solver

[https://github.com/material-foundation/material-color-utilities/blob/main/dart/lib/hct/src/hct_solver.dart#L64]()

This array is copied into the final JS code. It's about **~4700 bytes**. If we can find the formulae to generate the value on the fly, we could save some space.

## Keyboard mapping

There is an enum listing all the possible keys we can pressed.

`,Lang1:144,Lang2:145,Lang3:146,Lang4:147,Lang5:148,LaunchApp1:149,LaunchApp2:150`

Some of the keys are not available with every keyboards. We should provide some configurations to reduce those values depending of the localization of the user.
