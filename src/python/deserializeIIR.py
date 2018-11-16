import IIR_pb2
import textwrap
import sys
import argparse 

class deserializer:
  def __init__(self, metadata):
    self.indent_=0
    self.T_ = textwrap.TextWrapper(initial_indent=' '*self.indent_, width=120,subsequent_indent=' '*self.indent_)
    self.metadata_ = metadata
 
  def visitBuiltinType(self, builtin_type):
    if builtin_type.type_id == 0:
      raise ValueError('Builtin type not supported')
    elif builtin_type.type_id == 1:
      return "auto"
    elif builtin_type.type_id == 2:
      return "bool"
    elif builtin_type.type_id == 3:
      return "int"
    elif builtin_type.type_id == 4:
      return "float"
    raise ValueError('Builtin type not supported')

  def visitUnaryOperator(self, expr):
    return expr.op+" " +self.visitExpr(expr.operand)
  def visitBinaryOperator(self, expr):
    return self.visitExpr(expr.left) + " " + expr.op + " " + self.visitExpr(expr.right) 
  def visitAssignmentExpr(self, expr):
    return self.visitExpr(expr.left) + " " + expr.op + " " + self.visitExpr(expr.right)
  def visitTernaryOperator(self, expr):
    return "(" + self.visitExpr(expr.cond) + " ? " + self.visitExpr(expr.left) + " : " + self.visitExpr(expr.right) + ")"
  def visitVarAccessExpr(self, expr):
    return expr.name  #+ self.visitExpr(expr.index)
  def visitFieldAccessExpr(self, expr):
    str_ = expr.name +"["
    str_ += ",".join(str(x) for x in expr.offset)
    str_ += "]"
    return str_ 
  def visitLiteralAccessExpr(self, expr):
    return expr.value
  # call to external function, like math::sqrt
  def visitFunCallExpr(self, expr):
    return expr.callee + "("+",".join(self.visitExpr(x) for x in expr.arguments)+")"
  def visitExpr(self,expr):
    if expr.WhichOneof("expr") == "unary_operator":
      return self.visitUnaryOperator(expr.unary_operator)
    elif expr.WhichOneof("expr") == "binary_operator":
      return self.visitBinaryOperator(expr.binary_operator)
    elif expr.WhichOneof("expr") == "assignment_expr":
      return self.visitAssignmentExpr(expr.assignment_expr)
    elif expr.WhichOneof("expr") == "ternary_operator":
      return self.visitTernaryOperator(expr.ternary_operator)
    elif expr.WhichOneof("expr") == "fun_call_expr":
      return self.visitFunCallExpr(expr.fun_call_expr)
    elif expr.WhichOneof("expr") == "stencil_fun_call_expr":
      raise ValueError("non supported expression")
    elif expr.WhichOneof("expr") == "stencil_fun_arg_expr":
      raise ValueError("non supported expression")
    elif expr.WhichOneof("expr") == "var_access_expr":
      return self.visitVarAccessExpr(expr.var_access_expr)
    elif expr.WhichOneof("expr") == "field_access_expr":
      return self.visitFieldAccessExpr(expr.field_access_expr)
    elif expr.WhichOneof("expr") == "literal_access_expr":
      return self.visitLiteralAccessExpr(expr.literal_access_expr)
    else:
      raise ValueError("Unknown expression")

  def visitVarDeclStmt(self, var_decl):
    str_=""
    if var_decl.type.WhichOneof("type")=="name":
      str_+=var_decl.type.name
    elif var_decl.type.WhichOneof("type")=="builtin_type":
      str_ += self.visitBuiltinType(var_decl.type.builtin_type)
    else:
      raise ValueError("Unknown type ", var_decl.type.WhichOneof("type"))
    str_ += " " + var_decl.name

    if var_decl.dimension != 0:
      str_ += "["+str(var_decl.dimension)+"]"

    str_ += var_decl.op
 
    for expr in var_decl.init_list:
      str_ += self.visitExpr(expr)

    print(self.T_.fill(str_))
  def visitExprStmt(self,stmt):
    print(self.T_.fill(self.visitExpr(stmt.expr)))
  def visitIfStmt(self, stmt):
    cond = stmt.cond_part
    if cond.WhichOneof("stmt") != "expr_stmt":
      raise ValueError("Not expected stmt")

    print(self.T_.fill("if("+self.visitExpr(cond.expr_stmt.expr)+")"))
    self.visitBodyStmt(stmt.then_part)
    self.visitBodyStmt(stmt.else_part)

  def visitBlockStmt(self, stmt):
    print(self.T_.fill("{"))
    self.indent_+=2
    self.T_.initial_indent=' '*self.indent_

    for each in stmt.statements:
      self.visitBodyStmt(each)
    self.indent_-=2
    self.T_.initial_indent=' '*self.indent_

    print(self.T_.fill("}"))

  def visitBodyStmt(self, stmt):
    if stmt.WhichOneof("stmt") == "var_decl_stmt":
      self.visitVarDeclStmt(stmt.var_decl_stmt)
    elif stmt.WhichOneof("stmt") == "expr_stmt":
      self.visitExprStmt(stmt.expr_stmt)
    elif stmt.WhichOneof("stmt") == "if_stmt":
      self.visitIfStmt(stmt.if_stmt)
    elif stmt.WhichOneof("stmt") == "block_stmt":
      self.visitBlockStmt(stmt.block_stmt)
    else:
      raise ValueError("Stmt not supported :" + stmt.WhichOneof("stmt"))
  def visitInterval(self, interval):
    str_=""
    if (interval.WhichOneof("LowerLevel") == 'special_lower_level'):
      if interval.special_lower_level == 0:
        str_ += "kstart"
      else:
        str_ += "kend"
    elif  (interval.WhichOneof("LowerLevel") == 'lower_level'):
      str_ += str(interval.lower_level)
    str_ += ","
    if (interval.WhichOneof("UpperLevel") == 'special_upper_level'):
      if interval.special_upper_level == 0:
        str_ += "kstart"
      else:
        str_ += "kend"
    elif  (interval.WhichOneof("UpperLevel") == 'upper_level'):
      str_ += str(interval.upper_level)
    return str_

  def visitStatement(self, stmt):

    self.indent_+=2
    self.T_.initial_indent=' '*self.indent_

    self.visitBodyStmt(stmt.ASTStmt)

    self.indent_-=2
    self.T_.initial_indent=' '*self.indent_
  
  def visitAccess(self, accessid, extents, mode):
    extent_str = ""
    for extent in extents.extents:
      if not extent_str:
        extent_str="{"
      else:
        extent_str +=","
      extent_str += str(extent.minus)+","+str(extent.plus)

    extent_str +="}"
    print(self.T_.fill(mode+": " +self.metadata_.AccessIDToName[accessid])) + extent_str 

  def visitAccesses(self, accesses):

    print(self.T_.fill("Accesses: "))
    self.indent_+=2
    self.T_.initial_indent=' '*self.indent_

    for accessid,extents in accesses.writeAccess.iteritems():
      self.visitAccess(accessid, extents,"w")
    for access in accesses.readAccess.iteritems():
      self.visitAccess(accessid,extents,"r")

    self.indent_-=2
    self.T_.initial_indent=' '*self.indent_
    

  def visitDoMethod(self, domethod):
    domethodName = "DoMethod_"+str(domethod.DoMethodID)

    domethodName += "("+self.visitInterval(domethod.interval)+")"

    print(self.T_.fill(domethodName))
    self.indent_+=2
    self.T_.initial_indent=' '*self.indent_

    for stmtaccess in domethod.stmtaccesspairs:
#      self.visitAccesses(stmtaccess.callerAccesses)
      self.visitStatement(stmtaccess.statement)

    self.indent_-=2
    self.T_.initial_indent=' '*self.indent_

 
  def visitStage(self, stage):
    stagename = "stage_"+str(stage.stageID) 

    print(self.T_.fill(stagename))
    self.indent_+=2
    self.T_.initial_indent=' '*self.indent_

    for domethod in stage.domethods:
      self.visitDoMethod(domethod)

    self.indent_-=2
    self.T_.initial_indent=' '*self.indent_

  def visitMultiStage(self, ms):
    msname = "multistage_"+str(ms.MulitStageID)
    if ms.looporder == 0:
      msname += "<forward>"
    elif ms.looporder == 1:
      msname += "<backward>"
    elif ms.looporder == 3:
      msname += "<parallel>"
    print(self.T_.fill(msname))
    self.indent_+=2
    self.T_.initial_indent=' '*self.indent_

    for stage in ms.stages:
      self.visitStage(stage)

    self.indent_-=2
    self.T_.initial_indent=' '*self.indent_

  def visitStencil(self,stencil):
    print(self.T_.fill(self.metadata_.stencilName+"_"+str(stencil.stencilID)))
    self.indent_+=2
    self.T_.initial_indent=' '*self.indent_

    for ms in stencil.multistages:
      self.visitMultiStage(ms)
 
    self.indent_-=2
    self.T_.initial_indent=' '*self.indent_
      
  def visitFields(self,fields): 
    str_="field "
    for field in fields:
      str_ += field.name
      dims = ["i","j","k"]
      dims_=[]
      for i in range(1,3):
        if field.field_dimensions[i] != -1:
          dims_.append(dims[i])
      str_ += str(dims_)
      str_ += ","
    print(self.T_.fill(str_))




parser=argparse.ArgumentParser(
    description='''Deserializes a google protobuf file encoding an HIR example and traverses the AST printing a DSL code with the user equations''',
)
#parser.add_argument('--hir', type=string, help='FOO!')
parser.add_argument('hirfile',type=argparse.FileType('rb'), help='google protobuf HIR file')
args=parser.parse_args()

stencilInstantiation = IIR_pb2.StencilInstantiation()

stencilInstantiation.ParseFromString(args.hirfile.read())
args.hirfile.close()


T = textwrap.TextWrapper(initial_indent=' '*1, width=120,subsequent_indent=' '*1)
des = deserializer(stencilInstantiation.metadata)

for stencil in stencilInstantiation.internalIR.stencils:
  des.visitStencil(stencil)

