<?php
/**
 * @file parse.php
 * @author Zhamilya Abikenova (xabike00)
 */

//***********CLASS********//
// for handling the scanned line containing all methods to properly parse it.
class LineClass {
    public $string;
    public $par_type = [];
    public $par_value = [];
    public $param;
    public $instruction;
    public $parameterscount = 0;
    public $partype;
    public $frame;

    //STATP expansion
    public $jump;
    public $com;
    public $labels_all = "";
    public $label_count;



    //function to parse one line
    public function parseLine($str){
        $this->string=$str;
        if(preg_match('/\s*#.*$/', $this->string)) {
            if (preg_match('/#.*/', $this->string)) {
                $this->com++;
            }
            $this->string = preg_replace('/\s*#.*$/', '', $this->string);

        }

        $this->string = trim(preg_replace('/\s+/', ' ', $this->string));
        $this->instruction = strtoupper(trim(explode(' ', $this->string,2)[0]));

        if(preg_match('/^(CREATEFRAME|PUSHFRAME|POPFRAME|BREAK|RETURN)\s*$/',$this->string)) //these functions have no parameters so no tokenizing of those can occur
        {
            $this->param = "";
        }
        else
        {
            $this->param = explode(' ', $this->string, 2)[1];
        }

        if($this->param!=""){
            foreach (explode(' ', $this->param) as $par) {
                if(!(preg_match('/@/', $par))) {
                    $this->parameterscount++;
                    array_push($this->par_type,"type");
                    array_push($this->par_value,trim($par));
                }
                else {
                    $this->parameterscount++;
                    array_push($this->par_type, explode('@', $par, 2)[0]);
                    array_push($this->par_value, trim(explode('@', $par, 2)[1]));
                }
            }
        }
    }

    public function genXML($counter){ //Method used to generate XML code from the scanned line.

        $xml_body= "\t<instruction order=\"".$counter."\" opcode=\"".$this->instruction."\">\n";
        for ($i = 0; $i < $this->parameterscount; $i++) {
            if ($this->par_type[$i] == 'LF' || $this->par_type[$i] == 'GF' || $this->par_type[$i] == 'TF') {
                $this->partype="var";
                $this->frame=$this->par_type[$i]."@";
            }
            elseif ($this->instruction == 'CALL' || $this->instruction == 'LABEL' || $this->instruction == 'JUMP'){
                    $this->partype = "label";
            }
            elseif (($this->instruction =='JUMPIFEQ' && $this->par_type[$i] == 'type') || $this->instruction =='JUMPIFNEQ' && $this->par_type[$i] == 'type'){
                $this->partype = "label";
            }
            else {
                $this->partype=$this->par_type[$i];
                $this->frame="";
            }
            $xml_body=$xml_body."\t\t<arg".($i+1)." type=\"".$this->partype."\">".$this->frame.$this->par_value[$i]."</arg".($i+1).">\n";
        }
        return $xml_body."\t</instruction>\n";
    }

    /// METHODS TO CHECK VALIDITY OF ARGUMENT VALUES
    // always check argument type, then maching argument value rules. 
    public function funcNil($arg) {
        if ($this->par_type[$arg] == 'nil') {
            if (preg_match('/^nil$/', $this->par_value[$arg])){
                return true;
            } else return false;
        } else return false;
    }

    public function funcInt($var) {
        if ($this->par_type[$var] == 'int') {
            if (preg_match('/^[-|+]?[0-9]+$/', $this->par_value[$var])){
                return true;
            } else return false;
        } else return false;
    }

    public function funcBool($var) {
        if ($this->par_type[$var] == 'bool') {
            if (preg_match('/^true$/', $this->par_value[$var]) || preg_match('/^false$/', $this->par_value[$var])){
            return true;
            } else return false;
        } else return false;
    }

    public function funcString($var) { //replacing XML sensitive characters
        $this->par_value[$var] = str_replace('&','&amp;', $this->par_value[$var]);
        $this->par_value[$var] = str_replace('<','&lt;', $this->par_value[$var]);
        $this->par_value[$var] = str_replace('>','&gt;', $this->par_value[$var]);
        if ($this->par_type[$var] == 'string') {
            if (preg_match('/^([^#\\\\]|\\\\\d\d\d)*$/', $this->par_value[$var])){
                return true;
            } else return false;
        } else return false;
    }

    public function funcVar($var) {
        if ($this->par_type[$var] == 'LF' || $this->par_type[$var] == 'GF' || $this->par_type[$var] == 'TF') {
            if (preg_match('/^[a-zA-Z_\-$&%*!?][a-zA-Z0-9_\-$&%*!?]*$/', $this->par_value[$var])){
                $this->par_value[$var] = str_replace('&','&amp;', $this->par_value[$var]);
                if((preg_match('/[&amp]/', $this->par_value[$var])) || (preg_match('/^[a-zA-Z_\-$&%*!?][a-zA-Z0-9_\-$&%*!?]*$/', $this->par_value[$var]))){
                    return true;
                }
            } else return false;
        } else return false;
    }

    
    public function funcLabel($arg) {
        if (preg_match('/^[a-zA-Z_\-$&%*!?][a-zA-Z0-9_\-$&%*!?]*$/', $this->par_value[$arg])){
            return true;
        } else return false;
    }

    
    public function funcType($arg) {
        if ($this->par_type[$arg] == 'type') {
            if ($this->par_value[$arg] == 'string' || $this->par_value[$arg] == 'int' || $this->par_value[$arg] == 'bool'){
                return true;
            } else return false;
        } else return false;
    }
    /// METHODS TO CHECK VALIDITY OF ARGUMENT VALUES END
    
    /// METHODS TO CHECK CORRECT ARGUMENT COUNT 
    //check count and call methods to check validity of argument subtypes {symb,var,label}
    public function _operandZero() {
        if ($this->parameterscount <> 0){
            errorCode(23);
        }

    }

    public function _operandOne(){
        if ($this->parameterscount == 1) {
            if($this->instruction == 'DEFVAR' || $this->instruction == 'POPS' ) {
               if (!$this->funcVar(0)) {
                   errorCode(23);
               }
            } elseif ($this->instruction == 'CALL' || $this->instruction == 'LABEL' || $this->instruction == 'JUMP') {
                if (!($this->funcLabel(0) && $this->par_type[0] == 'type')) {
                    errorCode(23);
                }
            } elseif ($this->instruction == 'PUSHS' || $this->instruction == 'WRITE' || $this->instruction == 'EXIT' || $this->instruction == 'DPRINT') {
                if (!($this->funcVar(0) || $this->funcString(0) || $this->funcNil(0) || $this->funcBool(0) || $this->funcInt(0))) {
                    errorCode(23);
                }
            } else errorCode(23);
        } else errorCode(23);
    }

    public function _operandTwo() {
        if ($this->parameterscount == 2) {
            if ($this->instruction == 'MOVE'|| $this->instruction == 'NOT' || $this->instruction == 'INT2CHAR' || $this->instruction == 'STRLEN' || $this->instruction == 'TYPE') {
                if ($this->funcVar(0)) {
                    if (!($this->funcVar(1) || $this->funcString(1) || $this->funcNil(1) || $this->funcBool(1) || $this->funcInt(1))) {
                        errorCode(23);
                    }
                } else errorCode(23);
            }
            elseif ($this->instruction == "READ") {
                if ($this->funcVar(0)) {
                    if (!$this->funcType(1)) {
                        errorCode(23);
                    }
                } else errorCode(23);
            } else errorCode(23);
        } else errorCode(23);
    }

    public function _operandThree() {
        if ($this->parameterscount == 3) {
            switch ($this->instruction) {
                case 'ADD':
                case 'SUB':
                case 'MUL':
                case 'IDIV':
                case 'LT':
                case 'GT':
                case 'EQ':
                case 'AND':
                case 'OR':
                case 'STRI2INT':
                case 'CONCAT':
                case 'SETCHAR':
                case 'GETCHAR':
                    if($this->funcVar(0)) {
                        if ($this->funcVar(1) || $this->funcString(1) || $this->funcNil(1) || $this->funcBool(1) || $this->funcInt(1)) {
                            if (!($this->funcVar(2) || $this->funcString(2) || $this->funcNil(2) || $this->funcBool(2) || $this->funcInt(2))) {
                                errorCode(23);
                            }
                        } else errorCode(23);
                    } else errorCode(23);
                    break;
                case 'JUMPIFEQ':
                case 'JUMPIFNEQ':
                    if ($this->funcLabel(0) && $this->par_type[0] == 'type'){
                        if ($this->funcVar(1) || $this->funcString(1) || $this->funcNil(1) || $this->funcBool(1) || $this->funcInt(1)) {
                            if (!($this->funcVar(2) || $this->funcString(2) || $this->funcNil(2) || $this->funcBool(2) || $this->funcInt(2))) {
                                errorCode(23);
                            }
                        } else errorCode(23);
                    } else errorCode(23);
                    break;
            }
        } else errorCode(23);
    }    
    ///METHODS TO CHECK CORRECT ARGUMENT COUNT  END

    public function _operandCounter() { //method to check if instruction name and the number of arguments is correct
        switch ($this->instruction) {
            case 'CREATEFRAME':
            case 'PUSHFRAME':
            case 'POPFRAME':
            case 'BREAK':
                $this->_operandZero();
                break;
            case 'RETURN':
                $this->jump++;
                $this->_operandZero();
                break;
            case 'DEFVAR':
            case 'PUSHS':
            case 'POPS':
            case 'WRITE':
            case 'EXIT':
            case 'DPRINT':
                $this->_operandOne();
                break;
            case 'LABEL':
                $this->labels_all = $this->par_value[0];
                $this->label_count++;
                $this->_operandOne();
                break;
            case 'JUMP':
            case 'CALL':
                $this->jump++;
                $this->_operandOne();
                break;
            case 'MOVE':
            case 'NOT':
            case 'INT2CHAR':
            case 'READ':
            case 'STRLEN':
            case 'TYPE':
                $this->_operandTwo();
                break;
            case 'ADD':
            case 'SUB':
            case 'MUL':
            case 'IDIV':
            case 'LT':
            case 'GT':
            case 'EQ':
            case 'AND':
            case 'OR':
            case 'STRI2INT':
            case 'CONCAT':
            case 'SETCHAR':
            case 'GETCHAR':
                $this->_operandThree();
                break;
            case 'JUMPIFEQ':
            case 'JUMPIFNEQ':
                $this->jump++;
                $this->_operandThree();
                break;

            default:
                errorCode(22);
        }
    }
}

    //***********************ERROR**********************//
    function errorCode($error) {
        fprintf(STDERR, $error);
        exit($error);
    }

    //***********************ARGUMENTS+STATP************//

    //variables for bonus task STATP
    $statistic = false;
    $statp = array("--loc", "--comments", "--labels", "--jumps");

    //control argument value "--help"
    if ($argc > 1 && $argc <= 6) {
        if($argv[1] == '--help') {
            if($argc > 2) {
                errorCode(10);
            }
            echo "---------------------HELP----------------------------\n";
            echo "Script parse.php loads source code from a specified file,\n";
            echo "parses and further inspects the code's lexical and syntactic\n";
            echo "correctness, after which it is translated to an XML variant.\n";

            echo "Command --stats= <file> writes statistic to output file\n ";
            echo "To check --stats you can use:\n";
            echo "\t--loc - prints number of instruction\n";
            echo "\t--comments - prints number of comments\n";
            echo "\t--jumps - prints number of instruction\n";
            echo "\t--labels - prints number of unique labels\n";
            echo "--------------------------------------------------------\n";
            exit(0);
        }
        elseif(preg_match('/--stats=/', $argv[1])){
            $statistic = true;
            for($i = 2; $i < $argc; $i++) {
                if(!(in_array($argv[$i], $statp))){
                    errorCode(10); //not correct argument
                }
            }
        }
        else {
            errorCode(10); //not correct argument --help
        }
    }
    elseif ($argc > 6) {
        errorCode(10); //not correct count of arguments
    }
    if($statistic) {
        $file_stat = fopen((preg_replace('/--stats=/','', $argv[1])), 'w' );
        if(!$file_stat) {
            errorCode(12); //can't open file
        }
    }

    $loc = 0;
    $comments = 0;
    $jumps = 0;
    $labels = 0;
    $label_array = [];


    //***********************HEADER************//


    $file = fopen('php://stdin', "r");
    if (!$file) {
        errorCode(11); //can't open IPPcode20.txt
    }
    $first_line = fgets($file);

    //if before header whitespaces or comments
    while(preg_match('/^(\s*#.*$|\s*$)/', $first_line)) {
        if (preg_match('/#.*/', $first_line)) {
            $comments++;
        }
        $first_line = fgets($file);
    }
    //controls for header in first line
    if(preg_match('/^\s*\.ippcode20($|\s*#.*$|\s*$)/i',$first_line))
    {
        if (preg_match('/#.*/', $first_line)) {
            $comments++;
        }
        while (preg_match('/\s*#.*$/', $first_line)) {
            $first_line = preg_replace('/\s*#.*$/', '', $first_line);
            if (preg_match('/#.*/', $first_line)) {
                $comments++;
            }
        }
    }
    else {
        errorCode(21);
    }

    $xml_string = "<?xml version=\"1.0\" encoding=\"UTF-8\"?>\n<program language=\"IPPcode20\">\n"; //apply header
    $counter = 0;

    while(1)
    {
        $line = new LineClass();
        $string = fgets($file); //scanning a line from stdin
        if(!$string) //EOF
        {
            echo $xml_string."</program>";
            //write statistics to output file $file_stat
            if($statistic && $file_stat){
                for ($i = 2; $i < $argc; $i ++){
                    switch ($argv[$i]){
                        case "--loc":
                            fprintf($file_stat, $loc."\n");
                            break;
                        case "--comments":
                            fprintf($file_stat, $comments."\n");
                            break;
                        case "--labels":
                            fprintf($file_stat, $labels."\n");
                            break;
                        case "--jumps":
                            fprintf($file_stat, $jumps."\n");
                            break;
                        default:
                            errorCode(10);
                    }
                }
                fclose($file_stat);
            }
            exit(0);
        }

        while(preg_match('/^(\s*#.*|\s*)$/', $string)){ //skipping empty lines or lines with only comments, while counting any comments found
            if (preg_match('/#.*/', $string)) {
                $comments++;
            }
            $string = fgets($file);
            //EOF
            if(!$string){
                echo $xml_string."</program>";
                //write statistics to output file $file_stat
                if($statistic && $file_stat){
                    for ($i = 2; $i < $argc; $i ++){
                        switch ($argv[$i]){
                            case "--loc":
                                fprintf($file_stat, $loc."\n");
                                break;
                            case "--comments":
                                fprintf($file_stat, $comments."\n");
                                break;
                            case "--labels":
                                fprintf($file_stat, $labels."\n");
                                break;
                            case "--jumps":
                                fprintf($file_stat, $jumps."\n");
                                break;
                            default:
                                errorCode(10);
                        }
                    }
                    fclose($file_stat);
                }
                exit(0);
            }
        }

        $line->parseLine($string); //line of text to be tokenized
        $line->_operandCounter(); //check the tokenized's line validity
        $counter++;
        $xml_string=$xml_string.$line->genXML($counter); //string containing the XML code.

        if($line->jump){
            $jumps+= $line->jump;
        }
        if($line->com){
            $comments+= $line->com;
        }
        if($line->label_count) {
            array_push($label_array,$line->labels_all);
            $labels = count(array_count_values(array_unique($label_array)));
        }
        $loc = $counter;
    }

    ?>