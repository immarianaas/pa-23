package dk.dtu.pa.Teacher;

public interface Teacher {

    abstract class Subject {
        protected int subjectCode;

        protected Subject(int subj) {
            this.subjectCode = subj;
        }

        public abstract String favouriteSubject();

        public int getSubjectCode(){
            return this.subjectCode;
        }
    }
}
