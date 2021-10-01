import React from 'react';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import { faReply } from "@fortawesome/free-solid-svg-icons";


interface ReplyButtonProps {
  replyButtonClickCallback(): any;
}


export default class ReplyButton extends React.Component<ReplyButtonProps, {}> {
  render(): JSX.Element {
    return (
      <i onClick={this.props.replyButtonClickCallback}><FontAwesomeIcon icon={faReply} className="reply-button" /></i>
    )
  }
}