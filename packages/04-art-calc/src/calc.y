/* art-calc: калькулятор целочисленных выражений (bison) */
%{
#include <stdio.h>
int yylex(void);
void yyerror(const char *s);
%}

%define parse.error verbose
%token NUM
%left '+' '-'
%left '*' '/' '%'
%precedence NEG

%%
input:
    %empty
  | input line
  ;

line:
    '\n'
  | expr '\n'        { printf("%ld\n", $1); }
  | error '\n'       { yyerrok; }
  ;

expr:
    NUM
  | expr '+' expr    { $$ = $1 + $3; }
  | expr '-' expr    { $$ = $1 - $3; }
  | expr '*' expr    { $$ = $1 * $3; }
  | expr '/' expr    { if ($3) $$ = $1 / $3; else { yyerror("division by zero"); $$ = 0; } }
  | expr '%' expr    { if ($3) $$ = $1 % $3; else { yyerror("division by zero"); $$ = 0; } }
  | '-' expr %prec NEG { $$ = -$2; }
  | '(' expr ')'     { $$ = $2; }
  ;
%%

void yyerror(const char *s)
{
    fprintf(stderr, "art-calc: %s\n", s);
}

int main(void)
{
    return yyparse();
}
