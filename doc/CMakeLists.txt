include(UseLATEX)

add_latex_document(main.tex
  INPUTS example.tex  expression_elements.tex  intro.tex  macro.tex  main.tex root_element.tex statement_elements.tex 
         common_elements.tex
)
