import { Router } from '@angular/router';
import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import { AuthService } from '../auth/auth.service';

@Component({
  selector: 'app-header',
  standalone: true,
  imports: [CommonModule],
  templateUrl: './header.component.html',
  styleUrls: ['./header.component.scss']
})
export class HeaderComponent {
  isDarkMode = false;
  isLoggedIn: boolean = false;
  isLoading = false;

  constructor(
    private router: Router,
    private authService: AuthService
  ) {}

  toggleDarkMode(){
    this.isDarkMode = !this.isDarkMode;
    const root = document.documentElement;
    if (this.isDarkMode) {
      root.classList.add('dark');
      localStorage.setItem('theme', 'dark');
    } else {
      root.classList.remove('dark');
      localStorage.setItem('theme', 'light');
    }
  }

  gotToHome() {
    this.router.navigate(['/']);
  }

  login() {
    this.isLoading = true;
    setTimeout(() => {
      this.isLoading = false;
      this.router.navigate(['auth/login']);
    }, 1200)
  }

  logout() {
    this.isLoading = true;
    this.authService.logout();
    setTimeout(() => {
      this.isLoading = false;
      this.router.navigate(['/']);
    }, 1200)
  }

  ngOnInit() {
    const saveTheme = localStorage.getItem('theme');
    if (saveTheme === 'dark') {
      document.documentElement.classList.add('dark')
    }
  }
}
