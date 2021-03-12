export default class Survey {
    key!: string;
    title!: string;
    results_secret!: string;
    admin_secret!: string;
    viewsNumber: number;
    votersNumber: number;
    questionersNumber: number;
    date!: string;


    constructor(key: string, title: string, results_secret: string, admin_secret: string, viewsNumber: number, votersNumber: number, commentatorsNumber: number) {
        this.key = key;
        this.title = title;
        this.results_secret = results_secret;
        this.admin_secret = admin_secret;
        this.viewsNumber = viewsNumber;
        this.votersNumber = votersNumber;
        this.questionersNumber = commentatorsNumber;
        this.date = new Date().toString();
    }

    getUrl() {
        return `surveys/${this.key}`;
    }
}