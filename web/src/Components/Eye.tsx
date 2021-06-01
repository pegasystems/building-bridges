import React from 'react';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import { faEye, faEyeSlash } from "@fortawesome/free-solid-svg-icons";


interface EyeProps {
    slashed: boolean;
    hideOrShowCallback(): any;
}


export default class Eye extends React.Component<EyeProps, {}> {
    render(): JSX.Element {
      return (
        <i onClick = {this.props.hideOrShowCallback}><FontAwesomeIcon icon={this.props.slashed ? faEyeSlash : faEye} className="hide-eye"/></i>
      )
    }
  }