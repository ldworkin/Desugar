# Description:

A tiny Python script to expand or "desugar" Haskell do blocks. 

You can also ask lambdabot on the IRC channel to @undo expressions;
this was written mostly for my own understanding, and with the
intention of expanding the functionality later.

As of now, the capabilities are very limited. Most notably,
you cannot use pure code in the do blocks (such as let statements). 

## Dependencies:

[Pyparsing](http://pyparsing.wikispaces.com/)

## Usage:

Provide the do block as the first (and only) command line argument. 
If no arguments are provided, you will be prompted for input.

## Examples:

do { x1 <- eval x; x2 <- eval y; safediv x1 x2 } gives
eval x >>= (\x1 -> eval y >>= (\x2 -> safediv x1 x2))

do { x <- xs; y <- ys; return (x,y) } gives
xs >>= (\x -> ys >>= (\y -> return (x,y)))

do { x <- getChar ; y <- getChar; print [x,y]; return True } gives
getChar >>= (\x -> getChar >>= (\y -> print [x,y] >> return True))


