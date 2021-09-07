import { camelizeKeys } from 'humps';
import { UserVote } from ".";

export default class QuestionModel {
    _id!: string;
    content!: string;
    isAuthor!: boolean;
    hideVotes!: boolean;
    isAnonymous!: boolean;
    authorFullName: string = '';
    authorEmail: string = '';
    authorNickname: string = '';
    upvotes: number = 0;
    downvotes: number = 0;
    voted: UserVote = UserVote.None;
    read: string = 'false';
    hidden: boolean = false;

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
        for (const [key, value] of Object.entries(camelizeKeys(questionDict, function (key, convert) {
            return key === '_id' ? key : convert(key);
        }))) {
            (question as any)[key] = value
        }

        question.hideVotes = question.upvotes == null && question.read === 'false';
        return question;
    }
}
