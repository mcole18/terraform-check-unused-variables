locals {
    a = concat(var.one)
    b = [var.one]
}

resource "aws_instance" "test" {
  ami           = "hi-mom"
  instance_type = "${var.one}-${aws_instance.test.ami}"

  tags = {
    Name = var.module_two
    Env  = "svar.eight"
  }
}
