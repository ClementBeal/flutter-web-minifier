# Literal reduction

## `true` and `false`

Replace respectally with `!0` and `!1`

## Float factorisation

Some float numbers can be replace by the fractionnal notation

`0.00104420466` becomes `3/2873`

/!\ Check if the fraction length is smaller than the float

# Shorten the float

Replace `0.xxxxx...` with `.xxxxx....`

## Scientific notation

Replace numbers like `0.1` or `0.001` with `1e-1` and `1e-3` when the result is shorter

## Number repeatition

Some value like `3.14` are used several times. Put them into a new variable and use it everywhere.
