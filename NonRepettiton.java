 class NonRepeatedCharFirst {
    
    static int func(String inputStr){
       int rep=0; 
     for(char i:inputStr.toCharArray()){
        if ( inputStr.indexOf(i) == inputStr.lastIndexOf(i)) {
            rep=inputStr.indexOf(i);
            break;
        }
        
    }
    if (rep==0){
            return -1;
        }
        else{
            return rep;
        }
    }
    
    public static  void main(String args[]) {
     
  System.out.println(func("aabb"));
       
        }
}