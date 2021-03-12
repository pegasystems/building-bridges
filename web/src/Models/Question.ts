import { UserVote } from ".";

export default class QuestionModel {
    _id!: string;
    content!: string;
    isAuthor!: boolean;
    hideVotes!: boolean;
    upvotes: number = 0;
    downvotes: number = 0;
    voted: UserVote = UserVote.None;
    read: string = 'false';

    addUserVote(voteType: UserVote) {
        if (voteType === UserVote.Up) {
            this.upvotes++;
            this.downvotes -= Number(this.voted !== UserVote.None);
            this.voted = UserVote.Up;
        } else {
            this.downvotes++;
            this.upvotes -= Number(this.voted !== UserVote.None);
            this.voted = UserVote.Down;
        }
    }

    removeUserVote(): void {
        if (this.voted === UserVote.Up) {
            this.upvotes--;
        }
        else {
            this.downvotes--;
        }
    }

    toggleRead(): void {
        this.read = this.read === 'true' ? 'false' : 'true'
    }
    
    static createQuestionFromApiResult(questionDict: any): QuestionModel {
        let question = new QuestionModel();
        question.content = questionDict.content;
        question.downvotes = questionDict.downvotes;
        question.upvotes = questionDict.upvotes;
        question.isAuthor = questionDict.isAuthor;
        question.voted = questionDict.voted;
        question._id = questionDict._id;
        question.read = questionDict.read;

        question.hideVotes = question.upvotes == null && question.read === 'false';
        return question;
    }
}
