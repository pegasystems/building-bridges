import React from 'react';
import './Footer.css';

interface FooterState {
  contactEmail: string
}

export default class Footer extends React.Component<{}, FooterState> { 

  state = {
    contactEmail: ''
  }

  componentDidMount() {
    this.getContactEmail();
  }

  getContactEmail() {
      fetch('/api/info/email')
      .then(result => {
        if (!result.ok) {
          throw new Error("Couldn't get footer info.")
        }
        return result.text()
      })
      .then(data => {
        this.setState({contactEmail: data.replace(/\s/g, "").replaceAll('"', "").replaceAll('\'', "")});
      });
  }

  render(): JSX.Element {
    return(
      this.state.contactEmail != null && this.state.contactEmail !== '' ?
      <footer className="App-footer">
        <div>
          <p>If you encounter any issues, please contact us
             at <a href={"mailto:" + this.state.contactEmail}>{this.state.contactEmail}</a>.</p>
        </div>
      </footer> : <></>
    );
  }
}
