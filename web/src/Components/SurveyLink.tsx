import React from 'react';

interface SurveyLinkProps {
    link: string
}

interface SurveyLinkState {
    textToShow: string
}

export default class SurveyLink extends React.Component<SurveyLinkProps, SurveyLinkState> {
    state = {
        textToShow: 'Copy link',
    }

    copyToClipboard = () => {
        const textField = document.createElement('textarea');
        textField.innerText = this.props.link;
        document.body.appendChild(textField);
        textField.select();
        document.execCommand('copy');
        textField.remove();
        this.setState({textToShow: 'Copied!'});
        setTimeout(() => {
            this.setState({textToShow: 'Copy link'});
        }, 2000);
    };

    render(): JSX.Element {
        return (<i className="copy" onClick={this.copyToClipboard}>{this.state.textToShow}</i>);
    }
}
