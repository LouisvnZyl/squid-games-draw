import { Component } from '@angular/core';
import { Router } from '@angular/router';

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.scss'],
})
export class AppComponent {
  constructor(private readonly router: Router) {}

  public onOpenStream() {
    void this.router.navigateByUrl('streaming');
  }
}
