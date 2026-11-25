/* art-calc: лексический анализатор (flex) */
%option noyywrap nounput noinput
%{
#include <stdlib.h>
#define YYSTYPE long
#include "calc.tab.h"
%}

%%
[0-9]+          { yylval = strtol(yytext, NULL, 10); return NUM; }
[ \t]+          ;
\n              { return '\n'; }
.               { return yytext[0]; }
%%
