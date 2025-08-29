import { filter } from 'rxjs';
import { CommonModule } from '@angular/common';
import { Component, OnInit } from '@angular/core';
import { AuthService } from './auth/auth.service';
import { HeaderComponent } from './header/header.component';
import { Router, RouterOutlet, NavigationEnd } from '@angular/router';

@Component({
  selector: 'app-root',
  imports: [RouterOutlet, CommonModule, HeaderComponent],
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.scss']
})
export class AppComponent implements OnInit {
  title = 'frontend';
  showHeader = true;
  constructor(
    private router: Router,
    private authService: AuthService
  ) {
      this.router.events
      .pipe(filter(event => event instanceof NavigationEnd))
      .subscribe((event: any) => {
        const noHeader = ['auth/login', '/dashboard'];
        this.showHeader = !noHeader.includes(event.urlAfterRedirects);
      })
  }
  ngOnInit(): void {
    this.authService.syncAuthStatus();
  }
}