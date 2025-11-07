class Main {

  public static void main(String[] args) {
    
    int first = {{ .Values.hull.config.specific.insert_into_template_code_1 }};
    int second = {{ .Values.hull.config.specific.insert_into_template_code_2 }};

    int sum = first + second;
    System.out.println(first + " + " + second + " = "  + sum);
  }
}