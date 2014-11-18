
package task.learning;

import java.util.Arrays;
import java.util.Objects;
import java.util.StringTokenizer;
import task.Task.Consts;

/**
 *
 * @author Ivchenko Oleg (Kirius VeLKerr)
 */
public class Element {
    
    public enum Type {
        LOW{
            @Override
            public String nameLugBoot() {
                return "small";
            }
        },
        MED {
            @Override
            public String nameLugBoot() {
                return "med";
            }
        },
        HIGH {
            @Override
            public String nameLugBoot() {
                return "big";
            }
        },
        VHIGH{
            @Override
            public String nameLugBoot() {
                return "ERROR!!!";
            }
        },
        UNDEFINED{
            @Override
            public String nameLugBoot() {
                return name();
            }
        };
        
        public abstract String nameLugBoot();
        public boolean isDefined(){
            return (this != null) && (this != UNDEFINED);
        }
    }
    protected Type[] enumCoeffs; //buying, maint, safety
    protected int[] intCoeffs; //doors, person
    private Acceptability acceptability;
    
    public Element(String str){
        enumCoeffs = new Type[4];
        intCoeffs = new int[2];
        StringTokenizer st = new StringTokenizer(str, Consts.DELIMITER);
        for(int i=0; i<2; i++){
            enumCoeffs[i] = getEnum(Type.class, st.nextToken());
        }
        intCoeffs[0] = Integer.parseInt(st.nextToken().substring(0, 1));
        String pers = st.nextToken();
        if(pers.equals("more")){
            intCoeffs[1] = 5;
        }
        else{
            intCoeffs[1] = Integer.parseInt(pers);
        }
        enumCoeffs[2] = getLugBoot(st.nextToken());
        enumCoeffs[3] = getEnum(Type.class, st.nextToken());
        acceptability = getEnum(Acceptability.class, st.nextToken());
    }
    
    protected Element(){
        intCoeffs = new int[]{0, 0};
        enumCoeffs = new Type[4];
        Arrays.fill(enumCoeffs, Type.UNDEFINED);
    }
    
    private static <K extends Enum<K>> K getEnum(Class<K> enumClass, String str){
        for(K el: enumClass.getEnumConstants()){
            if(el.name().toLowerCase().equals(str)){
                return el;
            }
        }
        return null;
    }
    
    private static Type getLugBoot(String str){
        for(Type p: Type.values()){
            if(p.nameLugBoot().equals(str)){
                return p;
            }
        }
        return null;
    }
    
    public final Acceptability contains(Classificator cl){
        for(int i=0; i<enumCoeffs.length; i++){
            if(cl.enumCoeffs[i] != Type.UNDEFINED && cl.enumCoeffs[i] != enumCoeffs[i]){
                return null;
            }
        }
        return acceptability;
    }
    
    public final Classificator intersect(Element e){
        Classificator res = new Classificator();
        for(int i=0; i<enumCoeffs.length; i++){
            if(enumCoeffs[i] == e.enumCoeffs[i]){
                res.enumCoeffs[i] = enumCoeffs[i];
            }
        }
        for(int i=0; i<intCoeffs.length; i++){
            if(intCoeffs[i] == e.intCoeffs[i]){
                res.intCoeffs[i] = intCoeffs[i];
            }
        }
        return res;
    }
    
    @Override
    public String toString(){
        StringBuilder sb = new StringBuilder();
        String def = "|";
        for(int i=0; i<2; i++){
            if(enumCoeffs[i] != null){
                sb.append(enumCoeffs[i].name().toLowerCase());
            }
            else{
                sb.append(def);
            }
            sb.append(Consts.DELIMITER);
        }
        if(intCoeffs[0] > 0){
            sb.append(intCoeffs[0]);
            if(intCoeffs[0] == 5){
                sb.append("more");
            }
        }
        else{
            sb.append(def);
        }
        sb.append(Consts.DELIMITER);
        if(intCoeffs[1] > 0){
            if(intCoeffs[1] == 5){
                sb.append("more");
            }
            else{
                sb.append(intCoeffs[1]);
            }
        }
        else{
            sb.append(def);
        }
        sb.append(Consts.DELIMITER);
        if(enumCoeffs[2] != null){
            sb.append(enumCoeffs[2].nameLugBoot());
        }
        else{
            sb.append(def);
        }
        sb.append(Consts.DELIMITER);
        if(enumCoeffs[3] != null){
            sb.append(enumCoeffs[2].name().toLowerCase());
        }
        else{
            sb.append(def);
        }
        sb.append(Consts.DELIMITER);
        if(acceptability != null){
            sb.append(acceptability.name().toLowerCase());
        }
        else{
            sb.append(def);
        }
        return sb.toString();
    }

    @Override
    public int hashCode() {
        int hash = 7;
        hash = 41 * hash + Arrays.deepHashCode(this.enumCoeffs);
        hash = 41 * hash + Arrays.hashCode(this.intCoeffs);
        hash = 41 * hash + Objects.hashCode(this.acceptability);
        return hash;
    }

    @Override
    public boolean equals(Object obj) {
        if (obj == null) {
            return false;
        }
        if (getClass() != obj.getClass()) {
            return false;
        }
        final Element other = (Element) obj;
        if (!Arrays.deepEquals(this.enumCoeffs, other.enumCoeffs)) {
            return false;
        }
        return Arrays.equals(this.intCoeffs, other.intCoeffs);
    }

    public Acceptability getAcceptability() {
        return acceptability;
    }
}
